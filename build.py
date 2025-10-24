#!/usr/bin/env python3
"""
Build automation script for PyInstaller.
"""

import subprocess
import sys

def build_executable():
    try:
        # Optimize for size: exclude unnecessary modules, use UPX if available
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--exclude-module', 'matplotlib',
            '--exclude-module', 'tkinter.test',
            '--exclude-module', 'test',
            '--exclude-module', 'unittest',
            '--exclude-module', 'pdb',
            '--exclude-module', 'pydoc',
            '--strip',
            'main.py'
        ]
        subprocess.run(cmd, check=True)
        print("Build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")

if __name__ == "__main__":
    build_executable()