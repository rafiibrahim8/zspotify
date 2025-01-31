import requests
import base64
from mutagen import id3
from mutagen.flac import Picture
from mutagen._file import File

class AudioTagger:
    
    def __init__(self):
        pass

    def set_audio_tags(self, fullpath, full_info, artists=None, name=None, album_name=None, release_year=None,
                       disc_number=None, track_number=None, track_id_str=None, album_artist=None, image_url=None):
        """sets music_tag metadata using mutagen if possible"""
        
        album_artist = album_artist or artists  # Use artists if album_artist is None

        extension = str(fullpath).split('.')[-1]

        if extension == 'mp3':
            self._set_mp3_tags(fullpath, artists, name, album_name, release_year, disc_number,
                               track_number, track_id_str, album_artist, image_url)
        else:
            self._set_other_tags(fullpath, full_info, artists, name, album_name, release_year, disc_number,
                                 track_number, track_id_str, image_url)

    def _set_mp3_tags(self, fullpath, artist, name, album_name, release_year, disc_number, 
                      track_number, track_id_str, album_artist, image_url):
        tags = id3.ID3(fullpath)

        mp3_map = {
            "TPE1": artist,
            "TIT2": name,
            "TALB": album_name,
            "TDRC": release_year,
            "TDOR": release_year,
            "TPOS": str(disc_number) if disc_number else None,
            "TRCK": str(track_number) if track_number else None,
            "COMM": "https://open.spotify.com/track/" + track_id_str if track_id_str else None,
            "TPE2": album_artist,
        }

        for tag, value in mp3_map.items():
            if value:
                tags[tag] = id3.Frames[tag](encoding=3, text=value)

        if image_url:
            albumart = requests.get(image_url).content
            if albumart:
                tags["APIC"] = id3.APIC(encoding=3, mime="image/jpeg", type=3, desc="0", data=albumart)

        tags.save()

    def get_album_artists(self, track_info):
        return ", ".join([artist["name"] for artist in track_info["album"]["artists"]])

    def _set_other_tags(self, fullpath, full_info, artist, name, album_name, release_year, disc_number, 
                        track_number, track_id_str, image_url):
        
        track_info = full_info["tracks"][0]
        total_tracks = track_info["album"]["total_tracks"]
        
        tags = File(fullpath, easy=False)

        tag_map = {
            "artist": artist,
            "albumartist": self.get_album_artists(track_info),
            "title": name,
            "date": track_info["album"]["release_date"],
            "encodedby": "Spotify",
            "album": album_name,
            "comment": "https://open.spotify.com/track/" + track_id_str if track_id_str else None,
            "discnumber": str(disc_number) if disc_number else None,
            "tracknumber": str(track_number).strip().zfill(len(str(total_tracks))),
            "tracktotal": str(total_tracks),
            "woas": "https://open.spotify.com/track/" + track_id_str if track_id_str else None,
            "isrc": track_info["external_ids"]["isrc"],
        }

        for tag, value in tag_map.items():
            if value is not None:
                tags[tag] = value

        if image_url:
            res = requests.get(image_url)
            assert res.status_code < 300, f"Error downloading album art: {res.status_code}"
            
            picture = Picture()
            picture.type = 3
            picture.desc = "Cover"
            picture.mime = res.headers["Content-Type"]
            picture.data = res.content
            image_data = picture.write()

            encoded_data = base64.b64encode(image_data)
            vcomment_value = encoded_data.decode("ascii")
            tags["metadata_block_picture"] = [vcomment_value]
        
        try:
            tags.save()
        except Exception as e:
            if 'unable to read full header' not in str(e):
                raise
