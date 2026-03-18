# Audio Conversion Guide - Converting to WAV Format

## Why Convert to WAV?

- **No dependencies**: WAV files work with BirdNET without ffmpeg
- **Most reliable**: Best compatibility with librosa and BirdNET
- **Simple format**: Uncompressed, widely supported

## Conversion Methods

### Method 1: Using ffmpeg (Command Line)

If you have ffmpeg installed:

```bash
# Convert MP3 to WAV
ffmpeg -i input.mp3 output.wav

# Convert FLAC to WAV
ffmpeg -i input.flac output.wav

# Convert any format to WAV
ffmpeg -i input.any output.wav
```

**Install ffmpeg** (if not installed):
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Method 2: Using Python (pydub)

If you have pydub installed (already in your environment):

```python
from pydub import AudioSegment

# Convert MP3 to WAV
audio = AudioSegment.from_mp3("input.mp3")
audio.export("output.wav", format="wav")

# Convert FLAC to WAV
audio = AudioSegment.from_file("input.flac")
audio.export("output.wav", format="wav")
```

**Quick Python script** - Save as `convert_to_wav.py`:

```python
#!/usr/bin/env python3
import sys
from pydub import AudioSegment

if len(sys.argv) < 2:
    print("Usage: python convert_to_wav.py input_file.mp3")
    sys.exit(1)

input_file = sys.argv[1]
output_file = input_file.rsplit('.', 1)[0] + '.wav'

try:
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")
    print(f"Converted {input_file} to {output_file}")
except Exception as e:
    print(f"Error: {e}")
    print("\nNote: For MP3/FLAC, you may need ffmpeg installed.")
    print("Install with: brew install ffmpeg (macOS)")
```

### Method 3: Online Converters (No Installation)

1. **CloudConvert**: https://cloudconvert.com/mp3-to-wav
   - Upload your file
   - Select WAV as output
   - Download converted file

2. **Online-Convert**: https://www.online-convert.com/
   - Choose audio converter
   - Upload file
   - Convert to WAV

3. **Zamzar**: https://www.zamzar.com/convert/mp3-to-wav/
   - Upload and convert
   - Download result

### Method 4: Using Audacity (GUI Application)

1. **Download Audacity**: https://www.audacityteam.org/
2. **Open your audio file**: File → Open
3. **Export as WAV**: File → Export → Export as WAV
4. **Choose settings**: 
   - Format: WAV (Microsoft)
   - Encoding: Signed 16-bit PCM (recommended)

### Method 5: macOS Built-in (QuickTime)

1. Open audio file in QuickTime Player
2. File → Export As → Audio Only
3. Choose format (may need to use another method for WAV)

## Recommended Settings for WAV

For BirdNET compatibility, use these settings:

- **Sample Rate**: 48000 Hz (or 44100 Hz)
- **Bit Depth**: 16-bit
- **Channels**: Mono or Stereo (both work)
- **Format**: PCM (uncompressed)

## Quick Test

After conversion, verify your WAV file:

```bash
# Check file info (if you have ffmpeg)
ffmpeg -i output.wav

# Or in Python
from pydub import AudioSegment
audio = AudioSegment.from_wav("output.wav")
print(f"Duration: {len(audio)/1000}s")
print(f"Sample rate: {audio.frame_rate}Hz")
print(f"Channels: {audio.channels}")
```

## Troubleshooting

### "File format not supported"
- Ensure the file is actually a valid audio file
- Try a different conversion method
- Check file isn't corrupted

### "Conversion failed"
- Install ffmpeg for MP3/FLAC conversion
- Use online converter as alternative
- Try a different source file

### "File too large"
- WAV files are uncompressed (larger than MP3)
- This is normal - WAV preserves quality
- BirdNET can handle large files

## For Your Project

Since you're using BirdNET in the web interface:

1. **Best approach**: Convert files to WAV before uploading
2. **Alternative**: Install ffmpeg to support MP3/FLAC directly
3. **Quick fix**: Use online converter if you just need to test

## Example Workflow

```bash
# 1. Convert your audio file
ffmpeg -i bird_recording.mp3 bird_recording.wav

# 2. Upload to BirdNET demo
# Use the web interface or:
python birdnet_demo.py bird_recording.wav --show-clip-integration
```

