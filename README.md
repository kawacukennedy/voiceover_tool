# Offline C++ TTS Voiceover Tool

A compact, high-quality, fully offline C++ application for neural text-to-speech synthesis and voiceover production.

## Features

- Fully offline operation
- Professional quality natural speech
- MP3 output at 320kbps CBR
- Multiple voice support
- CLI-first with optional GUI
- Low latency synthesis

## Building

### Prerequisites

- CMake 3.16+
- C++17 compiler
- ONNX Runtime
- libmp3lame
- Qt6 (optional for GUI)
- GoogleTest (optional for tests)

### Build Instructions

```bash
mkdir build
cd build
cmake -S .. -B . -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

## Usage

```bash
./tts synth --text "Hello world" --voice narrator --out hello.mp3
```

## License

MIT