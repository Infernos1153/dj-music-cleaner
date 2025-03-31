# DJ Music Cleaner & Downloader

A command-line tool to download playlists from Spotify or SoundCloud, clean up mp3 filenames by removing bracketed numbers, detect duplicates, and check for truncated files.

## Features
- Download playlists using `spotdl` for Spotify or `yt-dlp` for SoundCloud.
- Clean up mp3 filenames by removing numbers in brackets.
- Detect duplicate files and rename them.
- Check and optionally delete truncated files (duration < 30 seconds).
- Interactive mode with optional command-line flags for automation.

## Installation

### Prerequisites
- Python 3.6+
- `spotdl` (for Spotify downloads)
- `yt-dlp` (for SoundCloud downloads)
- `mutagen` (Python package)

### Using `curl` to install
Run the following command in your terminal:
```bash
curl -s https://raw.githubusercontent.com/yourusername/dj-music-cleaner/main/install.sh | bash