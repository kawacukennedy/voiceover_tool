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
- SSML support for prosody, emphasis, and breath
- Advanced audio post-processing: noise gate, compressor, limiter, silence trimming
- Automatic language detection and multilingual models
- Phoneme-level timing and subtitles export (SRT/VTT)
- Real-time streaming and PCM API
- Voice cloning pipeline with embedding extraction
- Batch processing and render queue
- Accessibility features: keyboard navigation, high contrast theme

## Installation

### Prerequisites

- Python 3.11 or 3.12 (Python 3.14 not yet supported by ONNX Runtime and Numba)
- pip

### Install Dependencies

Run the automated installer:

```bash
./install.sh
```

Or manually:

```bash
# Create virtual environment with compatible Python
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Troubleshooting

If you encounter compatibility issues:
- Ensure Python version is 3.11-3.13
- Update pip: `pip install --upgrade pip`
- For macOS: `brew install python@3.11` then use `python3.11 -m venv venv`

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