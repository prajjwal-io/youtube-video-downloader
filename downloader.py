"""
YouTube Video Downloader with Playlist Support
Downloads YouTube videos and playlists in the highest quality available
Requires: pip install yt-dlp
"""

import yt_dlp
import os
import sys
from pathlib import Path


def download_best_quality_video(url, output_path="./downloads"):
    """
    Download YouTube video in the best quality available
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the video
    """
    
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Configure for best quality download with optimized merging
    ydl_opts = {
        'format': 'bestvideo[height>=1080]+bestaudio/bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,  # Ensure single video download
        'merge_output_format': 'mp4',
        # Optimization options for faster processing
        'postprocessor_args': {
            'ffmpeg': ['-c:v', 'copy', '-c:a', 'copy']  # Copy streams, don't re-encode
        },
        'prefer_ffmpeg': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            print(f"📹 Title: {info.get('title', 'Unknown')}")
            print(f"⏱️  Duration: {info.get('duration', 'Unknown')} seconds")
            print(f"👤 Uploader: {info.get('uploader', 'Unknown')}")
            
            print("Downloading in best quality available...")
            ydl.download([url])
            print("✅ Download completed successfully!")
            
    except Exception as e:
        print(f"❌ Error downloading video: {str(e)}")
        return False
    
    return True


def download_playlist(url, output_path="./downloads"):
    """
    Download an entire YouTube playlist
    
    Args:
        url (str): YouTube playlist URL
        output_path (str): Directory to save videos
    """
    
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Configure for playlist download
    ydl_opts = {
        'format': 'bestvideo[height>=1080]+bestaudio/bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s'),
        'noplaylist': False,  # Enable playlist downloading
        'merge_output_format': 'mp4',
        'postprocessor_args': {
            'ffmpeg': ['-c:v', 'copy', '-c:a', 'copy']
        },
        'prefer_ffmpeg': True,
        'writeinfojson': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'extract_flat': False,  # Download all videos, not just metadata
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get playlist info first
            print("🔍 Extracting playlist information...")
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                playlist_title = info.get('title', 'Unknown Playlist')
                video_count = len(info['entries'])
                uploader = info.get('uploader', 'Unknown')
                
                print(f"📂 Playlist: {playlist_title}")
                print(f"👤 Creator: {uploader}")
                print(f"📊 Videos: {video_count}")
                
                # Ask for confirmation
                response = input(f"\nDownload all {video_count} videos? (y/n): ")
                if response.lower() != 'y':
                    print("❌ Download cancelled.")
                    return False
                
                print(f"\n⬇️  Starting download of {video_count} videos...")
                ydl.download([url])
                print(f"✅ Successfully downloaded {video_count} videos!")
                
            else:
                print("❌ No playlist found or single video detected.")
                print("💡 Use single video download for individual videos.")
                return False
                
    except Exception as e:
        print(f"❌ Error downloading playlist: {str(e)}")
        return False
    
    return True


def download_playlist_range(url, start=1, end=None, output_path="./downloads"):
    """
    Download a specific range of videos from a YouTube playlist
    
    Args:
        url (str): YouTube playlist URL
        start (int): Start video number (1-based)
        end (int): End video number (1-based), None for all remaining
        output_path (str): Directory to save videos
    """
    
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Configure playlist range
    playlist_items = f"{start}:{end}" if end else f"{start}:"
    
    ydl_opts = {
        'format': 'bestvideo[height>=1080]+bestaudio/bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s'),
        'noplaylist': False,
        'playlist_items': playlist_items,  # Specify range
        'merge_output_format': 'mp4',
        'postprocessor_args': {
            'ffmpeg': ['-c:v', 'copy', '-c:a', 'copy']
        },
        'prefer_ffmpeg': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"📊 Downloading videos {start} to {end or 'end'} from playlist...")
            ydl.download([url])
            print("✅ Playlist range download completed!")
            
    except Exception as e:
        print(f"❌ Error downloading playlist range: {str(e)}")
        return False
    
    return True


def download_multiple_videos(urls, output_path="./downloads"):
    """
    Download multiple YouTube videos in best quality
    
    Args:
        urls (list): List of YouTube video URLs
        output_path (str): Directory to save videos
    """
    
    success_count = 0
    
    for i, url in enumerate(urls, 1):
        print(f"\n📹 Downloading video {i}/{len(urls)}")
        print(f"URL: {url}")
        
        if download_best_quality_video(url, output_path):
            success_count += 1
    
    print(f"\n🎉 Downloaded {success_count}/{len(urls)} videos successfully!")


def detect_youtube_url_type(url):
    """
    Detect if YouTube URL is a playlist or single video
    """
    if any(keyword in url for keyword in ['playlist', 'list=']):
        return "playlist"
    else:
        return "video"


def main():
    """
    Main function - downloads YouTube videos with playlist support
    """
    
    if len(sys.argv) < 2:
        print("YouTube Video Downloader with Playlist Support")
        print("Usage:")
        print("  python3 downloader.py <URL1> [URL2] [URL3] ...")
        print("  python3 downloader.py --playlist <URL>      # Download entire playlist")
        print("  python3 downloader.py --range <URL> <start> <end>  # Download playlist range")
        print("\nExamples:")
        print("  # Single video")
        print("  python3 downloader.py 'https://www.youtube.com/watch?v=VIDEO_ID'")
        print("  # Entire playlist") 
        print("  python3 downloader.py --playlist 'https://www.youtube.com/playlist?list=PLAYLIST_ID'")
        print("  # Playlist range (videos 5-10)")
        print("  python3 downloader.py --range 'https://www.youtube.com/playlist?list=PLAYLIST_ID' 5 10")
        print("  # Multiple individual videos")
        print("  python3 downloader.py 'URL1' 'URL2' 'URL3'")
        return
    
    # Download entire playlist
    if '--playlist' in sys.argv:
        if len(sys.argv) < 3:
            print("❌ Please provide a playlist URL")
            return
        playlist_url = sys.argv[2]
        print(f"📂 Downloading entire YouTube playlist...")
        download_playlist(playlist_url)
        return
    
    # Download playlist range
    if '--range' in sys.argv:
        if len(sys.argv) < 5:
            print("❌ Please provide: --range <URL> <start> <end>")
            print("Example: --range 'PLAYLIST_URL' 1 10")
            return
        playlist_url = sys.argv[2]
        try:
            start = int(sys.argv[3])
            end = int(sys.argv[4]) if sys.argv[4] != 'end' else None
            print(f"📊 Downloading YouTube playlist range {start}-{end or 'end'}...")
            download_playlist_range(playlist_url, start, end)
        except ValueError:
            print("❌ Start and end must be numbers")
        return
    
    # Get URLs from command line arguments (filter out options)
    urls = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    
    if len(urls) == 1:
        url = urls[0]
        url_type = detect_youtube_url_type(url)
        
        print(f"🎯 Detected: YouTube {url_type}")
        
        if url_type == "playlist":
            print("💡 Detected playlist URL! Use --playlist for full playlist download")
            response = input("Download as single video instead? (y/n): ")
            if response.lower() == 'y':
                download_best_quality_video(url)
            else:
                print("Use: python3 downloader.py --playlist 'YOUR_URL'")
        else:
            download_best_quality_video(url)
    else:
        print(f"📦 Downloading {len(urls)} individual YouTube videos...")
        download_multiple_videos(urls)


if __name__ == "__main__":
    main()