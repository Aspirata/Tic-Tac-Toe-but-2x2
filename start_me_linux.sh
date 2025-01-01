#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python not found. Please install Python..."
    read -p "Press Enter to close this window..."
    exit 1
else
    echo "Python is already installed."
fi

pip install pyqt6

echo "Running game.py..."
python3 Scripts/game.py
pause