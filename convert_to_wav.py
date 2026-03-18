#!/usr/bin/env python3
"""
Quick audio conversion script to WAV format.
Usage: python convert_to_wav.py input_file.mp3
"""

import sys
import os

try:
    from pydub import AudioSegment
except ImportError:
    print("Error: pydub not installed.")
    print("Install with: pip install pydub")
    print("\nNote: For MP3/FLAC files, you also need ffmpeg:")
    print("  macOS: brew install ffmpeg")
    print("  Ubuntu: sudo apt-get install ffmpeg")
    sys.exit(1)

def convert_to_wav(input_file, output_file=None):
    """
    Convert audio file to WAV format.
    
    Args:
        input_file: Path to input audio file
        output_file: Path to output WAV file (optional)
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File not found: {input_file}")
    
    if output_file is None:
        # Generate output filename
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.wav"
    
    try:
        print(f"Converting {input_file} to WAV format...")
        
        # Load audio file
        audio = AudioSegment.from_file(input_file)
        
        # Export as WAV
        audio.export(output_file, format="wav")
        
        # Get file info
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        duration = len(audio) / 1000  # seconds
        
        print(f"✓ Successfully converted to: {output_file}")
        print(f"  Duration: {duration:.2f} seconds")
        print(f"  File size: {file_size:.2f} MB")
        print(f"  Sample rate: {audio.frame_rate} Hz")
        print(f"  Channels: {audio.channels}")
        
        return output_file
        
    except Exception as e:
        error_msg = str(e)
        if "ffmpeg" in error_msg.lower() or "avconv" in error_msg.lower():
            print("\nError: ffmpeg not found.")
            print("For MP3/FLAC files, you need ffmpeg installed:")
            print("  macOS: brew install ffmpeg")
            print("  Ubuntu: sudo apt-get install ffmpeg")
            print("\nAlternatively, use an online converter or convert to WAV first.")
        else:
            print(f"\nError: {error_msg}")
            print("\nTroubleshooting:")
            print("  - Ensure the input file is a valid audio file")
            print("  - Try a different audio file")
            print("  - For MP3/FLAC, install ffmpeg")
        raise

def main():
    if len(sys.argv) < 2:
        print("Audio to WAV Converter")
        print("=" * 50)
        print("\nUsage:")
        print("  python convert_to_wav.py input_file.mp3")
        print("  python convert_to_wav.py input_file.mp3 output.wav")
        print("\nSupported formats:")
        print("  - MP3 (requires ffmpeg)")
        print("  - FLAC (requires ffmpeg)")
        print("  - WAV (no conversion needed)")
        print("  - M4A (requires ffmpeg)")
        print("  - OGG (requires ffmpeg)")
        print("\nInstall ffmpeg:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu: sudo apt-get install ffmpeg")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        convert_to_wav(input_file, output_file)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()

