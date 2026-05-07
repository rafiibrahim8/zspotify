# Changelog

**v3.0.0 (07 May 2026)**
- Added pipx-first installation instructions for `git+https://github.com/rafiibrahim8/zspotify.git`.
- Updated package metadata for the 3.0.0 release.
- Pinned `librespot-python` to a specific commit for reproducible installs.
- Switched track metadata lookup to the internal librespot metadata helper.
- Added Spotify lyrics retrieval and improved lyric tagging for supported formats.
- Removed the `pydub` dependency and converted audio through FFmpeg directly.
- Preserved source audio by default with the `--audio-format source` option.
- Improved token refresh handling for authenticated Spotify API requests.
- Rewrote the README to match the current CLI, output layout, archive behavior, and dependency requirements.

**v2.1.0 (29 Sep 2023)**
- Use never python Docker image
- Rewrite classes, separate functionality

**v2.0.6 (31 Aug 2023)**
- added singles to downloads 
- fix artist albums tag for plex  

**v2.0.5 (22 May 2023)**
- Fixed issue caused by filenames being too long / Screeper

**v2.0.4 (18 May 2023)**
- Uprev librespot-org and set minimum version

**v2.0.3 (24 Apr 2023)**
- Show albums before downloading

**v2.0.1 (30 Mar 2023)**
- Refresh token on expiration / Screeper

**v2.0.0 (27 Mar 2023)**
- Major rewrite / Bionded
- Implement Python argparse / Bionded
- pip-ify zspotify / nicknitewolf

**v1.9.9 (03 Feb 2023)**
- Sort playlists by name / MauritzFunke

**v1.9.8 (01 Feb 2023)**
- Fix album without image / jlsalvador/fix-album-without-image
- Add egg name for librespot-python dependency (Fix) / scarlettekk

**v1.9.7 (29 Dic 2022)**
- Sum the size of the images, compares and saves the index of the largest image size

**v1.9.4 (14 Oct 2022)**
- Added cover 640x640

**v1.9.3 (30 Sep 2022)**
- Added KeyboardInterrupt control: Ctrl + C

**v1.9.2 (19 Aug 2022)**
- Added playlist_id support (https://github.com/VicDominguez)
- Fix -ls argument (https://github.com/axsddlr)
- Song Archive, to SKIP_PREVIOUSLY_DOWNLOADED (https://github.com/diebolo)

**v1.9.1 (19 Aug 2022)**
- Added extra option to download a playlist with the playlist-id. This playlist doesn't need be yours, it can be from other user.

**v1.9 (20 Jun 2022):**
- Fix fails at 87%

**v1.8 (23 Oct 2021):**
- Exclude album_type single
- Added progress bar for downloads.
- Changed welcome banner and removed unnecessary debug print statements.
- Show single progress bar for entire album.
- Added a small delay between downloading each track when downloading in bulk to help with downloading issues and potential bans.

**v1.7 (21 Oct 2021):**
- Added docker support
- Added range download example 1-10 example: SELECT ITEM BY ID: 1-10
- Added download all albums by artist
- Added subfolders for each disc
- Naming tracks: "artist - album - track-number. name"
- Setting Limit in 50 items

**v1.6 (20 Oct 2021):**
- Added Pillow to requirements.txt.
- Removed websocket-client from requirements.txt because librespot-python added it to their dependency list.
- Made it hide your password when you type it in.
- Added manual override to force premium quality if ZSpotify cannot auto-detect it.
- Added option to just download the raw audio with no re-encoding at all.
- Added Shebang line so it runs smoother on Linux.
- Made it download the entire track at once now so it is more efficient and fixed a bug users encountered.
