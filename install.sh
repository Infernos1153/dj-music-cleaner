#!/bin/bash

echo "Cloning the repo..."
git clone https://github.com/Infernos1153/dj-music-cleaner.git ~/dj-music-cleaner
cd ~/dj-music-cleaner

echo "Installing Python packages..."
pip3 install -r requirements.txt
pip3 install .

echo "🎉 Done!"
