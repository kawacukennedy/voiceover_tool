#!/bin/bash

# Installation script for Offline TTS Voiceover Tool

echo "Offline TTS Voiceover Tool Installer"
echo "====================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

if [[ "$PYTHON_VERSION" =~ ^3\.1[0-3]\. ]]; then
    echo "✓ Python $PYTHON_VERSION detected"
else
    echo "✗ Python $PYTHON_VERSION not supported. Please use Python 3.11-3.13"
    echo "On macOS: brew install python@3.11"
    echo "On Linux: apt install python3.11"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

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