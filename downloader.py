"""
YouTube Best Quality Video Downloader
Downloads videos in the highest quality available
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
        'noplaylist': True,
        'merge_output_format': 'mp4',
        # Optimization options for faster processing
        'postprocessor_args': {
            'ffmpeg': ['-c:v', 'copy', '-c:a', 'copy']  # Copy streams, don't re-encode
        },
        'prefer_ffmpeg': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading in 1080p+ quality (optimized)...")
            ydl.download([url])
            print("✅ Download completed successfully!")
            
    except Exception as e:
        print(f"❌ Error downloading video: {str(e)}")
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

def main():
    """
    Main function - downloads videos from command line arguments
    """
    
    if len(sys.argv) < 2:
        print("YouTube Best Quality Downloader")
        print("Usage:")
        print("  python downloader.py <URL1> [URL2] [URL3] ...")
        print("\nExample:")
        print("  python downloader.py 'https://www.youtube.com/watch?v=VIDEO_ID'")
        print("  python downloader.py 'URL1' 'URL2' 'URL3'")
        return
    
    # Get URLs from command line arguments
    urls = sys.argv[1:]
    
    if len(urls) == 1:
        download_best_quality_video(urls[0])
    else:
        download_multiple_videos(urls)

if __name__ == "__main__":
    main()