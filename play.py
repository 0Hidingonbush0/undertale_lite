#!/usr/bin/env python3
"""
Undertale Lite Game Launcher
"""

import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from undertale_lite import UndertaleLite

def main():
    """Launch the Undertale Lite game"""
    print("🎮 Starting Undertale Lite...")
    print("   Press Ctrl+C at any time to quit\n")
    
    game = UndertaleLite()
    game.run()

if __name__ == "__main__":
    main()