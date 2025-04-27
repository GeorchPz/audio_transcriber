# Audio Transcriber

A Python application for transcribing audio files to text using OpenAI's Whisper model, with features for saving transcriptions and metadata.

## Overview

Audio Transcriber is a tool that:
- Converts audio files to text transcriptions using Whisper (a free, open-source model that runs locally)
- Supports multiple languages (Spanish by default)
- Stores transcription data in both text files and H5 metadata files
- Provides utilities for batch processing multiple audio files

## Features

- **Audio Transcription**: Converts speech to text from various audio formats
- **Metadata Storage**: Saves detailed transcription data including:
  - Full text transcription
  - Language identification
  - Individual speech segments with timestamps
  - Confidence scores for transcriptions
- **File Management**: Handles file paths and organization automatically

## Dependencies

#### Python libraries used in this project:
- `numpy`: For optimal handling of numerical operations.
- `whisper`: For audio transcription.
- `pydub`: For audio file manipulation by `whisper`.
- `h5py`: For storing metadata in HDF5 format.

#### System requirements:
- `ffmpeg`: Required for audio processing (must be installed separately).


## Usage

### Basic Transcription

```python
from transcriber import AudioTranscriber

# Initialize with an audio file
transcriber = AudioTranscriber("my_audio.mp3", directory="my_files")

# Process the audio file
result = transcriber.process()

# Save the transcription
transcriber.txtsave()

# Save detailed metadata
transcriber.h5save()
```

*To load previously saved metadata:*
```python
# Initialize with the same audio file
transcriber = AudioTranscriber("my_audio.mp3", directory="my_files")

# Load the saved metadata
result = transcriber.h5load()
```