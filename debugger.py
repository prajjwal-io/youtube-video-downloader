#!/usr/bin/env python3
"""
YouTube Quality Debug Downloader
Helps diagnose quality issues and ensures best quality download
Requires: pip install yt-dlp
"""

import yt_dlp
import os
import sys
from pathlib import Path

def check_available_formats(url):
    """
    List all available formats for debugging
    """
    print("🔍 Checking available formats...\n")
    
    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            print(f"📹 Title: {info.get('title', 'Unknown')}")
            print(f"⏱️  Duration: {info.get('duration', 'Unknown')} seconds")
            print(f"👤 Uploader: {info.get('uploader', 'Unknown')}")
            print(f"📅 Upload Date: {info.get('upload_date', 'Unknown')}")
            
            formats = info.get('formats', [])
            if not formats:
                print("❌ No formats available")
                return
            
            print(f"\n📊 Available Formats ({len(formats)} total):")
            print("-" * 80)
            print(f"{'ID':<10} {'Extension':<10} {'Resolution':<12} {'FPS':<5} {'Codec':<10} {'Filesize':<12}")
            print("-" * 80)
            
            # Sort by quality (height, then fps)
            video_formats = []
            audio_formats = []
            
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('height'):  # Video formats
                    video_formats.append(f)
                elif f.get('acodec') != 'none':  # Audio formats
                    audio_formats.append(f)
            
            # Sort video formats by quality
            video_formats.sort(key=lambda x: (x.get('height', 0), x.get('fps', 0)), reverse=True)
            
            print("🎥 VIDEO FORMATS:")
            for f in video_formats[:10]:  # Show top 10 video formats
                format_id = f.get('format_id', 'N/A')
                ext = f.get('ext', 'N/A')
                height = f.get('height', 'N/A')
                width = f.get('width', 'N/A')
                fps = f.get('fps', 'N/A')
                vcodec = f.get('vcodec', 'N/A')[:10]
                filesize = f.get('filesize', 0)
                
                resolution = f"{width}x{height}" if width and height else str(height)
                filesize_str = f"{filesize/1024/1024:.1f}MB" if filesize else "N/A"
                
                print(f"{format_id:<10} {ext:<10} {resolution:<12} {fps:<5} {vcodec:<10} {filesize_str:<12}")
            
            print("\n🔊 AUDIO FORMATS:")
            audio_formats.sort(key=lambda x: x.get('abr', 0), reverse=True)
            for f in audio_formats[:5]:  # Show top 5 audio formats
                format_id = f.get('format_id', 'N/A')
                ext = f.get('ext', 'N/A')
                abr = f.get('abr', 'N/A')
                acodec = f.get('acodec', 'N/A')[:10]
                
                print(f"{format_id:<10} {ext:<10} {'Audio':<12} {abr:<5} {acodec:<10}")
            
            # Find the best quality
            best_video = max(video_formats, key=lambda x: (x.get('height', 0), x.get('fps', 0))) if video_formats else None
            if best_video:
                print(f"\n⭐ Best video format: {best_video.get('format_id')} - {best_video.get('width')}x{best_video.get('height')} @ {best_video.get('fps', 'N/A')} fps")
            
    except Exception as e:
        print(f"❌ Error checking formats: {str(e)}")

def download_highest_quality(url, output_path="./downloads", show_formats=False):
    """
    Download with multiple format options to ensure highest quality
    """
    
    if show_formats:
        check_available_formats(url)
        response = input("\nDo you want to continue with download? (y/n): ")
        if response.lower() != 'y':
            return
    
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Try multiple format strategies for maximum quality
    format_options = [
        # Best single file (video+audio combined)
        'best',
        # Best video + best audio (requires merging)
        'bestvideo+bestaudio/best',
        # Specific high quality formats
        'bestvideo[height>=1080]+bestaudio/bestvideo[height>=720]+bestaudio/best',
        # Fallback to any available format
        'worst'
    ]
    
    for i, format_str in enumerate(format_options):
        print(f"\n🎯 Trying format strategy {i+1}: {format_str}")
        
        ydl_opts = {
            'format': format_str,
            'outtmpl': os.path.join(output_path, '%(title)s [%(format_id)s].%(ext)s'),
            'noplaylist': True,
            'writeinfojson': True,  # Save metadata
            'writesubtitles': False,
            'writeautomaticsub': False,
            'embedsubs': False,
            'merge_output_format': 'mp4',  # Ensure MP4 output
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("⬇️  Downloading...")
                ydl.download([url])
                print("✅ Download completed successfully!")
                return True
                
        except Exception as e:
            print(f"❌ Strategy {i+1} failed: {str(e)}")
            if i < len(format_options) - 1:
                print("🔄 Trying next strategy...")
            continue
    
    print("❌ All download strategies failed!")
    return False

def main():
    if len(sys.argv) < 2:
        print("YouTube Quality Debug Downloader")
        print("Usage:")
        print("  python3 debug_downloader.py <URL> [--check-formats]")
        print("\nOptions:")
        print("  --check-formats    Show available formats before downloading")
        print("\nExamples:")
        print("  python3 debug_downloader.py 'https://www.youtube.com/watch?v=VIDEO_ID'")
        print("  python3 debug_downloader.py 'https://www.youtube.com/watch?v=VIDEO_ID' --check-formats")
        return
    
    url = sys.argv[1]
    show_formats = '--check-formats' in sys.argv
    
    if '--check-formats' in sys.argv and len(sys.argv) == 3:
        # Only show formats, don't download
        check_available_formats(url)
    else:
        download_highest_quality(url, show_formats=show_formats)

if __name__ == "__main__":
    main()