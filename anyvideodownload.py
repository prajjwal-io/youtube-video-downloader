"""
Universal Video Downloader
Downloads videos from YouTube and 1000+ other platforms
Requires: pip install yt-dlp
"""

import yt_dlp
import os
import sys
from pathlib import Path


def detect_platform(url):
    """
    Simple platform detection based on URL
    """
    if 'youtube.com' in url or 'youtu.be' in url:
        return "YouTube"
    elif 'vimeo.com' in url:
        return "Vimeo"
    elif 'tiktok.com' in url:
        return "TikTok"
    elif 'instagram.com' in url:
        return "Instagram"
    elif 'facebook.com' in url or 'fb.com' in url:
        return "Facebook"
    elif 'twitter.com' in url or 'x.com' in url:
        return "Twitter"
    elif 'twitch.tv' in url:
        return "Twitch"
    elif 'dailymotion.com' in url:
        return "Dailymotion"
    elif 'reddit.com' in url:
        return "Reddit"
    else:
        return "Unknown (but likely supported)"


def check_supported_platforms():
    """
    Display some of the popular supported platforms
    """
    platforms = [
        "YouTube", "Vimeo", "Dailymotion", "Twitch", "TikTok",
        "Instagram", "Facebook", "Twitter", "Reddit"
    ]
    
    print("🌐 Supported platforms include:")
    for i, platform in enumerate(platforms, 1):
        print(f"   {i:2d}. {platform}")
    print("   ... and 1000+ more!")
    print("\nJust paste any video URL and it will work!")


def download_best_quality_video(url, output_path="./downloads"):
    """
    Download video from any supported platform in the best quality available
    
    Supported platforms: YouTube, Vimeo, Dailymotion, Twitch, TikTok, Instagram, 
    Facebook, Twitter, Reddit, and 1000+ other sites
    
    Args:
        url (str): Video URL from any supported platform
        output_path (str): Directory to save the video
    """
    
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Configure for best quality download with platform-specific optimizations
    ydl_opts = {
        # Format selection optimized for different platforms
        'format': (
            # For YouTube and similar platforms with separate video/audio
            'bestvideo[height>=1080]+bestaudio/'
            'bestvideo[height>=720]+bestaudio/'
            'bestvideo+bestaudio/'
            # For platforms with combined formats
            'best[height>=1080]/'
            'best[height>=720]/'
            'best'
        ),
        'outtmpl': os.path.join(output_path, '%(title)s [%(extractor)s].%(ext)s'),
        'noplaylist': True,
        'merge_output_format': 'mp4',
        # Optimization options for faster processing
        'postprocessor_args': {
            'ffmpeg': ['-c:v', 'copy', '-c:a', 'copy']  # Copy streams, don't re-encode
        },
        'prefer_ffmpeg': True,
        # Extract metadata
        'writeinfojson': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            print(f"📹 Title: {info.get('title', 'Unknown')}")
            print(f"🌐 Platform: {info.get('extractor_key', 'Unknown')}")
            print(f"⏱️  Duration: {info.get('duration', 'Unknown')} seconds")
            print(f"👤 Uploader: {info.get('uploader', 'Unknown')}")
            
            print("Downloading in best quality available...")
            ydl.download([url])
            print("✅ Download completed successfully!")
            
    except Exception as e:
        print(f"❌ Error downloading video: {str(e)}")
        return False
    
    return True


def download_multiple_videos(urls, output_path="./downloads"):
    """
    Download multiple videos from any supported platforms in best quality
    
    Args:
        urls (list): List of video URLs from any supported platforms
        output_path (str): Directory to save videos
    """
    
    success_count = 0
    
    for i, url in enumerate(urls, 1):
        print(f"\n📹 Downloading video {i}/{len(urls)}")
        print(f"URL: {url}")
        platform = detect_platform(url)
        print(f"🎯 Detected platform: {platform}")
        
        if download_best_quality_video(url, output_path):
            success_count += 1
    
    print(f"\n🎉 Downloaded {success_count}/{len(urls)} videos successfully!")


def main():
    """
    Main function - downloads videos from command line arguments
    """
    
    if len(sys.argv) < 2:
        print("Universal Video Downloader")
        print("Downloads from YouTube, TikTok, Instagram, Vimeo, and 1000+ platforms")
        print("\nUsage:")
        print("  python anyvideodownload.py <URL1> [URL2] [URL3] ...")
        print("  python anyvideodownload.py --platforms    # Show supported platforms")
        print("\nExamples:")
        print("  python anyvideodownload.py 'https://www.youtube.com/watch?v=VIDEO_ID'")
        print("  python anyvideodownload.py 'https://vimeo.com/123456789'")
        print("  python anyvideodownload.py 'https://www.tiktok.com/@user/video/123'")
        print("  python anyvideodownload.py 'URL1' 'URL2' 'URL3'")
        return
    
    # Show platforms list
    if '--platforms' in sys.argv:
        check_supported_platforms()
        return
    
    # Get URLs from command line arguments
    urls = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    
    if len(urls) == 1:
        url = urls[0]
        platform = detect_platform(url)
        print(f"🎯 Detected platform: {platform}")
        download_best_quality_video(url)
    else:
        print(f"📦 Downloading {len(urls)} videos from multiple platforms...")
        download_multiple_videos(urls)


if __name__ == "__main__":
    main()