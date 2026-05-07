# ZSpotify

[![GPLv3](https://img.shields.io/github/license/rafiibrahim8/zspotify)](https://opensource.org/license/gpl-3-0)

ZSpotify is a command-line Spotify downloader. It can search Spotify or download
tracks, albums, playlists, artists, liked songs, podcast episodes, and complete
shows from Spotify URLs, Spotify URIs, or item IDs.

This fork uses `librespot-python` for Spotify login and audio retrieval, writes
metadata with `mutagen`, stores a JSON download archive, supports embedded
lyrics when Spotify returns them, and can either save the source audio stream or
convert it with FFmpeg.

## Requirements

- Python 3.9 or newer
- [pipx](https://pipx.pypa.io/) for isolated CLI installation
- FFmpeg available on `PATH` when converting audio to `mp3` or `ogg`
- A Spotify account

`--audio-format source` is the default and preserves the downloaded stream
without conversion. FFmpeg is still recommended, but it is only required when
you request conversion.

## Installation

### pipx recommended

`pipx` is recommended because it installs ZSpotify as an isolated command-line
app without mixing its dependencies into your project or system Python.

Install the current GitHub version:

```bash
pipx install git+https://github.com/rafiibrahim8/zspotify.git
```

Upgrade an existing pipx install:

```bash
pipx upgrade zspotify
```

If the `zspotify` command is not found after installation, make sure pipx's bin
directory is on your `PATH`:

```bash
pipx ensurepath
```

### pip

You can also install with pip. This is useful inside a virtual environment,
container, or other Python environment you manage yourself.

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install ZSpotify:

```bash
pip install git+https://github.com/rafiibrahim8/zspotify.git
```

Upgrade a pip install:

```bash
pip install --upgrade git+https://github.com/rafiibrahim8/zspotify.git
```

## First Run

Run ZSpotify once and sign in when prompted:

```bash
zspotify
```

By default, credentials are saved to:

```text
~/.zspotify/credentials.json
```

Use `--config-dir` to change the config directory, or `--credentials-file` to
point at a specific credentials file.

ZSpotify auto-detects Spotify account type. Premium accounts use very high
quality; free accounts use high quality. `--force-premium` overrides that
detection.

## Usage

Search interactively:

```bash
zspotify "artist or song name"
```

Download by URL:

```bash
zspotify "https://open.spotify.com/track/..."
zspotify "https://open.spotify.com/album/..."
zspotify "https://open.spotify.com/playlist/..."
```

Download by ID or URL with explicit options:

```bash
zspotify --track TRACK_ID_OR_URL
zspotify --album ALBUM_ID_OR_URL
zspotify --playlist PLAYLIST_ID_OR_URL
zspotify --artist ARTIST_ID_OR_URL
zspotify --episode EPISODE_ID_OR_URL
zspotify --full-show SHOW_ID_OR_URL
```

Download library items:

```bash
zspotify --liked-songs
zspotify --all-playlists
zspotify --select-playlists
```

Bulk download from a text file containing Spotify URLs:

```bash
zspotify --bulk-download urls.txt
```

Multiple IDs or URLs can be separated with commas or semicolons:

```bash
zspotify --track "TRACK_ID_1,TRACK_ID_2"
zspotify --album "ALBUM_ID_1;ALBUM_ID_2"
```

## CLI Reference

```text
usage: zspotify [-h] [-ap] [-sp] [-ls] [-pl PLAYLIST] [-tr TRACK]
                [-al ALBUM] [-ar ARTIST] [-ep EPISODE] [-fs FULL_SHOW]
                [-cd CONFIG_DIR] [--archive ARCHIVE] [-d DOWNLOAD_DIR]
                [-md MUSIC_DIR] [-pd EPISODES_DIR] [-v]
                [-af {mp3,ogg,source}] [--album-in-filename]
                [--antiban-time ANTIBAN_TIME]
                [--antiban-album ANTIBAN_ALBUM] [--limit LIMIT] [-f] [-ns]
                [-s] [-cf CREDENTIALS_FILE] [-bd BULK_DOWNLOAD]
                [search]

positional arguments:
  search                Search for a track, album, artist, or playlist, or
                        download by URL

options:
  -h, --help            Show help and exit
  -v, --version         Show the current ZSpotify version and exit
  -ap, --all-playlists  Download all saved playlists from your library
  -sp, --select-playlists
                        Select saved playlists from your library to download
  -ls, --liked-songs    Download your liked songs
  -pl PLAYLIST, --playlist PLAYLIST
                        Download playlist by ID or URL
  -tr TRACK, --track TRACK
                        Download track by ID or URL
  -al ALBUM, --album ALBUM
                        Download album by ID or URL
  -ar ARTIST, --artist ARTIST
                        Download all albums, compilations, and singles from an
                        artist by ID or URL
  -ep EPISODE, --episode EPISODE
                        Download podcast episode by ID or URL
  -fs FULL_SHOW, --full-show FULL_SHOW
                        Download all show episodes by ID or URL
  -cd CONFIG_DIR, --config-dir CONFIG_DIR
                        Folder for config files; default: ~/.zspotify
  --archive ARCHIVE     Archive filename inside the config directory; default:
                        archive.json
  -d DOWNLOAD_DIR, --download-dir DOWNLOAD_DIR
                        General download directory; default: current directory
  -md MUSIC_DIR, --music-dir MUSIC_DIR
                        Music download directory; default: current directory
  -pd EPISODES_DIR, --episodes-dir EPISODES_DIR
                        Podcast episode directory; default:
                        ~/Music/ZSpotify Podcast
  -af {mp3,ogg,source}, --audio-format {mp3,ogg,source}
                        Audio format: mp3, ogg, or source; default: source
  --album-in-filename   Include album name in generated filenames
  --antiban-time ANTIBAN_TIME
                        Seconds to wait between downloads; default: 10
  --antiban-album ANTIBAN_ALBUM
                        Seconds to wait between album, artist, or playlist
                        batches; default: 30
  --limit LIMIT         Search result limit; default: 10
  -f, --force-premium   Force premium quality handling
  -ns, --not-skip-existing
                        Do not skip existing files
  -s, --skip-downloaded
                        Skip IDs already present in the archive, even if the
                        file is missing from disk
  -cf CREDENTIALS_FILE, --credentials-file CREDENTIALS_FILE
                        Credentials file path; default:
                        ~/.zspotify/credentials.json
  -bd BULK_DOWNLOAD, --bulk-download BULK_DOWNLOAD
                        Download URLs listed in a text file
```

## Output Layout

Music downloads are written under `--music-dir`.

- Albums: `Artist/YYYY - Album/Track Number. Track Name`
- Multi-disc albums: `Artist/YYYY - Album/Disc Number/Track Number. Track Name`
- Playlists: `Playlist Name/Track Name`
- Liked songs: `Liked Songs/Artist - Track Name`

Podcast episodes are written under `--episodes-dir`.

Filenames are sanitized for common filesystem-problematic characters. Very long
filenames are shortened.

## Archive

Downloaded items are tracked in `archive.json` inside the config directory by
default. Use `--skip-downloaded` to skip anything already recorded there.

Older `.song_archive` files are migrated automatically from the configured
download paths when ZSpotify starts.

## Environment Variables

These environment variables provide defaults that can still be overridden with
CLI options:

```text
ANTI_BAN_WAIT_TIME=10
ANTI_BAN_WAIT_TIME_ALBUMS=30
LIMIT_RESULTS=10
```

## Notes

- Search currently returns tracks, albums, playlists, and artists.
- Podcast episodes and shows are supported by direct ID, URL, or URI.
- Spotify lyrics are embedded when available. Unsynced lyrics are written as
  plain lyrics; line-synced lyrics are written as synced/LRC-style metadata
  where the target file format supports it.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Disclaimer

This project is intended for personal use with content you are allowed to
access. Spotify may restrict or ban accounts that violate its terms. Use a
secondary account if you are concerned about account risk.

## License

ZSpotify is licensed under GPL-3.0-only. See [LICENSE](LICENSE).

## Acknowledgements

- [Footsiefat](https://github.com/Footsiefat) for the original ZSpotify
  implementation
- The upstream ZSpotify contributors whose work this fork builds on
