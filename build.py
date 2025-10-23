#!/usr/bin/env python3
"""
Build automation script for PyInstaller.
"""

import subprocess
import sys

def build_executable():
    try:
        subprocess.run([sys.executable, '-m', 'PyInstaller', '--onefile', 'main.py'], check=True)
        print("Build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")

if __name__ == "__main__":
    build_executable()