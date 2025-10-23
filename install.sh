#!/bin/bash

# Installation script for Offline TTS Voiceover Tool

echo "Offline TTS Voiceover Tool Installer"
echo "====================================="

# Check for compatible Python version
PYTHON_CMD=""
for cmd in python3.11 python3.12 python3.13 python3; do
    if command -v $cmd >/dev/null 2>&1; then
        VERSION=$($cmd --version 2>&1 | awk '{print $2}')
        if [[ "$VERSION" =~ ^3\.1[0-3]\. ]]; then
            PYTHON_CMD=$cmd
            PYTHON_VERSION=$VERSION
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "✗ No compatible Python version found (3.11-3.13 required)"
    echo "On macOS: brew install python@3.11"
    echo "On Linux: apt install python3.11"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected (using $PYTHON_CMD)"

# Check for tkinter
if ! $PYTHON_CMD -c "import tkinter" 2>/dev/null; then
    echo "⚠ Warning: Tkinter not available. GUI will not work."
    echo "On macOS: Install python-tk for the Python version:"
    echo "  brew install python-tk@3.12"
    echo "Then run this installer again."
else
    echo "✓ Tkinter available"
fi

# Create virtual environment
echo "Creating virtual environment..."
rm -rf venv  # Remove any existing venv
$PYTHON_CMD -m venv venv

# Activate and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Installation completed successfully!"
    echo ""
    echo "To use the app:"
    echo "  source venv/bin/activate"
    echo "  python main.py --help"
else
    echo "✗ Installation failed. Check error messages above."
    exit 1
fi