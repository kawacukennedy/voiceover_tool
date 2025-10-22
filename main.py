#!/usr/bin/env python3
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Offline TTS Voiceover Tool")
    parser.add_argument('--gui', action='store_true', help='Launch GUI')
    parser.add_argument('command', nargs='*', help='CLI command and arguments')
    args = parser.parse_args()

    if args.gui:
        from gui_main import gui_main
        gui_main()
    else:
        from cli import run_cli
        run_cli(args.command)

if __name__ == "__main__":
    main()