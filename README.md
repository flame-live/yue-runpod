# YuE Music Generation Model - RunPod Serverless

This fork adds RunPod serverless deployment support to the YuE music generation model.

## RunPod Setup

### Prerequisites
- A RunPod account
- HuggingFace account and token for model access
- Docker installed locally

### Deployment Steps

1. Build and push the container image to GitHub Container Registry:
   - Build: docker build -t ghcr.io/yourusername/yue-serverless:latest .
   - Push: docker push ghcr.io/yourusername/yue-serverless:latest

2. Create RunPod Serverless Endpoint:
   - Container: ghcr.io/yourusername/yue-serverless:latest
   - GPU: A100 80GB
   - Environment Variables: 
     HF_TOKEN=your_huggingface_token

3. Use the API:
   - Input format accepts:
     - genre: Genre tags (required)
     - lyrics: Song lyrics in sections (required)
     - audio_prompt: Base64 encoded audio file (optional)
     - start_time: Audio prompt start time in seconds (optional)
     - end_time: Audio prompt end time in seconds (optional)
   - Returns base64 encoded audio files

---

## Overview

YuE (乐) is a groundbreaking open-source foundation model for music generation, specifically for transforming lyrics into full songs. It generates complete songs with both vocal and accompaniment tracks, supporting diverse genres, languages, and vocal techniques.

## Features
- Text-to-music generation with genre and lyrics input
- Optional audio prompt for style reference
- Multi-language support (English, Mandarin, Cantonese, Japanese, Korean)
- Deployed as a RunPod serverless endpoint

## Hardware Requirements
- GPU: A100 80GB recommended
- For GPUs with less memory (24GB or less): limit to 2 sessions maximum

## Usage Example

Input format:
```json
{
    "genre": "inspiring female uplifting pop airy vocal",
    "lyrics": "[verse]\nSome lyrics here\n\n[chorus]\nMore lyrics here",
    "segments": 2,
    "batch_size": 4,
    "audio_prompt": "base64_encoded_audio",  // Optional
    "start_time": 0,                         // Optional
    "end_time": 30                           // Optional
}
```

## Original Project
For the original YuE project, visit: [YuE GitHub Repository](https://github.com/multimodal-art-projection/YuE)
