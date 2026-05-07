"""Map a librespot-python Metadata.Track protobuf into a Web API-shaped dict."""

from __future__ import annotations

from typing import Any

from librespot.core import Session
from librespot.metadata import AlbumId, ArtistId, TrackId


def _gid_to_b62(id_cls, gid: bytes) -> str:
    return id_cls.from_hex(gid.hex()).to_spotify_uri().split(':')[-1]


def _format_date(date) -> tuple[str, str]:
    if date.day:
        return f'{date.year:04d}-{date.month:02d}-{date.day:02d}', 'day'
    if date.month:
        return f'{date.year:04d}-{date.month:02d}', 'month'
    return f'{date.year:04d}', 'year'


def _artist_obj(artist) -> dict[str, Any]:
    b62 = _gid_to_b62(ArtistId, artist.gid)
    return {
        'external_urls': {'spotify': f'https://open.spotify.com/artist/{b62}'},
        'href': f'https://api.spotify.com/v1/artists/{b62}',
        'id': b62,
        'name': artist.name,
        'type': 'artist',
        'uri': f'spotify:artist:{b62}',
    }


def _is_playable(entity) -> bool:
    # Playable when there are no restrictions for the current market.
    # The embedded protobuf only carries restrictions when something applies,
    # so an empty list means unrestricted.
    return len(entity.restriction) == 0


def _album_obj(album, total_tracks: int | None = None) -> dict[str, Any]:
    b62 = _gid_to_b62(AlbumId, album.gid)
    release_date, precision = _format_date(album.date)

    images = [
        {
            'url': f'https://i.scdn.co/image/{img.file_id.hex()}',
            'width': img.width or None,
            'height': img.height or None,
        }
        for img in album.cover_group.image
    ]
    images.sort(key=lambda i: -(i['width'] or 0))

    album_type = album.type_str.lower() if album.type_str else None

    out: dict[str, Any] = {
        'album_type': album_type,
        'artists': [_artist_obj(a) for a in album.artist],
        'external_urls': {'spotify': f'https://open.spotify.com/album/{b62}'},
        'href': f'https://api.spotify.com/v1/albums/{b62}',
        'id': b62,
        'images': images,
        'is_playable': _is_playable(album),
        'name': album.name,
        'release_date': release_date,
        'release_date_precision': precision,
        'type': 'album',
        'uri': f'spotify:album:{b62}',
    }
    if total_tracks is not None:
        out['total_tracks'] = total_tracks
    return out


def get_track(track_id: str, session: Session) -> dict[str, Any]:
    """Fetch a track via librespot and return a Web API-shaped dict.

    `track_id` accepts either `spotify:track:<base62>` or the bare `<base62>`.
    """
    tid = (
        TrackId.from_uri(track_id)
        if track_id.startswith('spotify:track:')
        else TrackId.from_base62(track_id)
    )
    track = session.api().get_metadata_4_track(tid)

    b62 = _gid_to_b62(TrackId, track.gid)
    preview_url = (
        f'https://p.scdn.co/mp3-preview/{track.preview[0].file_id.hex()}' if track.preview else None
    )

    full_album = session.api().get_metadata_4_album(AlbumId.from_hex(track.album.gid.hex()))
    total_tracks = sum(len(disc.track) for disc in full_album.disc)

    return {
        'album': _album_obj(track.album, total_tracks=total_tracks),
        'artists': [_artist_obj(a) for a in track.artist],
        'disc_number': track.disc_number,
        'duration_ms': track.duration,
        'explicit': track.explicit,
        'external_ids': {e.type: e.id for e in track.external_id},
        'external_urls': {'spotify': f'https://open.spotify.com/track/{b62}'},
        'href': f'https://api.spotify.com/v1/tracks/{b62}',
        'id': b62,
        'is_local': False,
        'is_playable': _is_playable(track),
        'name': track.name,
        'popularity': track.popularity,
        'preview_url': preview_url,
        'track_number': track.number,
        'type': 'track',
        'uri': f'spotify:track:{b62}',
    }
