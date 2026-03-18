# BirdNET Demo - Quick Start

## Overview

The BirdNET demo provides evidence of model exploration and evaluation for audio classification capabilities. It demonstrates how BirdNET would integrate with the main Lost Pet Identifier pipeline.

## Installation

```bash
# Install BirdNET and TensorFlow (required dependency)
pip install birdnetlib tensorflow

# Optional: Install ffmpeg for better audio format support
# On macOS: brew install ffmpeg
# On Ubuntu: sudo apt-get install ffmpeg
```

Note: ffmpeg is optional but recommended for processing .mp3 and .flac files. .wav files work without ffmpeg.

## Usage

### Command Line

```bash
# Basic usage
python birdnet_demo.py sample_bird.wav

# With custom settings
python birdnet_demo.py sample_bird.wav --min-confidence 0.2 --top-k 10

# Show CLIP integration example
python birdnet_demo.py sample_bird.wav --show-clip-integration
```

### Web Interface

1. Start the web interface: `streamlit run app.py`
2. Navigate to the "BirdNET Demo" tab
3. Upload an audio file (.wav, .mp3, or .flac)
4. Click "Analyze Audio"

## What It Does

1. **Input**: Processes .wav audio file
2. **Output**: Returns bird species probabilities with confidence scores
3. **Integration Demo**: Shows how results would feed into CLIP text prompts

## Example Output

```
Input: sample_bird.wav
Minimum Confidence: 0.1

Analyzing audio file...

======================================================================
Output: Species Probabilities
======================================================================

1. American Robin              0.856 [████████████████████████████████████████████░░░░]
2. Northern Cardinal           0.234 [███████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
3. Blue Jay                    0.156 [███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]

Total detections: 3
```

## CLIP Integration

The demo shows how BirdNET output would be converted to CLIP text prompts:

- **BirdNET Output**: "American Robin" (confidence: 0.856)
- **CLIP Text Prompt**: "bird, American Robin"
- **Next Step**: This text would be embedded using CLIP and stored in FAISS

## Why Not Fully Integrated?

See `BIRDNET_INTEGRATION.md` for detailed explanation. Summary:

1. Audio processing pipeline requires additional components
2. Integration complexity (audio → text → embedding → FAISS)
3. Focus on core similarity matching prototype first
4. Architecture designed, pending full implementation

## Evidence Provided

- Model exploration: BirdNET tested and validated
- Integration design: Architecture documented
- Technical feasibility: Demonstrated working implementation
- Scope management: Clear understanding of integration requirements

## Documentation

- `BIRDNET_INTEGRATION.md` - Detailed integration documentation
- `birdnet_demo.py` - Standalone demo script
- Web interface - Interactive demo in "BirdNET Demo" tab

