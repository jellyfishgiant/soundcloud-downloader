# 🎵 soundcloud-downloader

A simple, fast Python tool to download tracks, playlists, likes, and reposts from SoundCloud — complete with metadata tag support.

## ✅ Features

- Download single tracks, playlists, user uploads, favorites, reposts, and comments.
- Sync-mode: only download new tracks or remove deleted ones.
- Metadata tagging: Title, Artist, Album artwork via Mutagen.
- Optional FLAC conversion (if lossless original available).
- Fully configurable via flags or config file.
- Cross‑platform: works on Python 3 (Windows/macOS/Linux).

---

## 🛠️ Installation

```bash
git clone https://github.com/jellyfishgiant/soundcloud-downloader.git
cd soundcloud-downloader
pip install -r requirements.txt
```

### Install FFmpeg (required for metadata and format conversion)

- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt-get install ffmpeg`
- Windows: [Download from ffmpeg.org](https://ffmpeg.org/)

---

## ⚙️ Configuration

You can create a config file at `~/.config/soundcloud-downloader/config.cfg`:

```ini
[DEFAULT]
client_id = YOUR_SOUNDCLOUD_CLIENT_ID
auth_token = OPTIONAL_OAUTH_TOKEN
download_path = ~/Music/SoundCloud
metadata = True
format = mp3
```

To get your `client_id`, inspect network calls from your browser while using SoundCloud.

---

## 📥 Usage

```bash
python downloader.py [OPTIONS]
```

### Common Options

| Option | Description |
|--------|-------------|
| `-l URL`         | Download track, playlist, or user profile |
| `-s QUERY`       | Search SoundCloud and download first result |
| `-n N`           | Download N most recent tracks |
| `-a`             | All uploads + reposts of a user |
| `-t`             | Only user uploads |
| `-f`             | Liked (favorite) tracks |
| `-C`             | Tracks the user commented on |
| `-p`             | Download playlists |
| `-r`             | Reposts only |
| `-c`             | Continue if file exists |
| `--download-archive FILE` | Use a log to skip duplicates |
| `--sync FILE`    | Sync content with archive file |
| `--flac`         | Convert lossless files to FLAC |
| `--onlymp3`      | Only download MP3 format |
| `--path DIR`     | Custom download path |
| `--name-format FORMAT` | Custom filename format |
| `--debug`, `--error` | Adjust log level verbosity |

### Examples

- Download a single track:
  ```bash
  python downloader.py -l https://soundcloud.com/user/track
  ```

- Download all favorites from a user:
  ```bash
  python downloader.py -l https://soundcloud.com/user -f
  ```

- Sync a playlist:
  ```bash
  python downloader.py -l https://soundcloud.com/user/sets/playlist --sync archive.txt
  ```

---

## 📚 Advanced Tips

- Use `--download-archive archive.txt` to avoid re-downloading.
- Use `--sync` for keeping playlists up to date.
- Use `--name-format "%(artist)s - %(title)s"` for custom filenames.
- Combine `--flac` with `--onlymp3` for selective format control.

---

## 👥 Contributing

1. Fork this repository
2. Create your branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-xyz`)
5. Create a new Pull Request

---

## 📄 License

MIT License. See the [LICENSE](LICENSE) file for more info.

---

## ⚠️ Disclaimer

This tool downloads tracks publicly available via SoundCloud's own web interface. Please respect copyright laws and use responsibly.
