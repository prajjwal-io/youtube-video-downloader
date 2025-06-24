# YouTube Video Downloader

A simple Python script to download YouTube videos in the highest quality available.

## Installation

### Prerequisites

You need Python 3.6 or higher installed on your system.

### Dependencies

#### 1. Install yt-dlp

**macOS:**
```bash
pip3 install yt-dlp
```

**Windows:**
```bash
pip install yt-dlp
```

**Linux:**
```bash
pip3 install yt-dlp
```

#### 2. Install FFmpeg (Required for best quality downloads)

**macOS:**
```bash
# Using Homebrew
brew install ffmpeg
```

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract the files
3. Add the `bin` folder to your system PATH
4. Or use Chocolatey: `choco install ffmpeg`

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL/Fedora
sudo dnf install ffmpeg
# or
sudo yum install ffmpeg
```

## Usage

### Basic Usage

**Download a single video:**
```bash
python3 downloader.py 'https://www.youtube.com/watch?v=VIDEO_ID'
```

**Download multiple videos:**
```bash
python3 downloader.py 'URL1' 'URL2' 'URL3'
```

### Examples

```bash
# Single video
python3 downloader.py 'https://www.youtube.com/watch?v=zjkBMFhNj_g'

# Multiple videos
python3 downloader.py 'https://www.youtube.com/watch?v=VIDEO1' 'https://www.youtube.com/watch?v=VIDEO2'
```

### Notes

- Videos are downloaded to the `downloads/` folder
- The script automatically selects the highest quality available
- Output format is MP4 for maximum compatibility
- Use single quotes around URLs to avoid shell interpretation issues

## Troubleshooting

**If you get permission errors on macOS/Linux:**
```bash
python3 downloader.py 'YOUR_URL'
```

**If Python 3 is not found:**
```bash
python downloader.py 'YOUR_URL'
```

**If FFmpeg is not found:**
- Make sure FFmpeg is properly installed and added to your system PATH
- Restart your terminal after installation