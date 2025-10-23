# Offline Python TTS Voiceover Tool

A compact, high-quality, fully offline Python application for neural text-to-speech synthesis and voiceover production using ONNX Runtime with quantized VITS models.

## Features

- Fully offline operation
- Professional quality natural speech suitable for narration and voiceover work
- MP3 output at 320kbps constant bitrate with ID3 metadata support
- Single-file distribution under 100MB for Linux, macOS, and Windows
- Multiple voice support via compact speaker embeddings
- Low latency synthesis with quantized ONNX models
- CLI-first user experience with optional minimal GUI built with Tkinter
- Reproducible builds with Poetry and PyInstaller

## Installation

### Prerequisites

- Python 3.11+
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### CLI

```bash
python main.py synth --text "Hello world" --voice narrator --out hello.mp3
```

Available commands:
- `synth`: Synthesize text to audio
- `synth-file`: Synthesize from text file
- `batch`: Batch synthesis from directory
- `list-voices`: List available voices
- `import-voice`: Import a voice embedding
- `preview-voice`: Preview a voice
- `server`: Start REST API server

### GUI

```bash
python gui_main.py
```

### REST API

Start server:
```bash
python main.py server
```

Endpoints:
- `GET /voices`: List voices
- `POST /synth`: Synthesize audio (JSON body: {"text": "hello", "voice": "narrator"})
- `GET /status`: Server status

## Building Executable

Using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

## Voices

Voices are stored in the `voices/` directory with `.bin` embeddings and `.json` metadata.

To import a voice:
```bash
python main.py import-voice path/to/embedding.bin --name myvoice
```

## License

MIT-compatible for application code with model license documented separately.