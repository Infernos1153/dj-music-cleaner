#!/bin/bash

echo "🔐 Admin privileges are needed. You may be prompted for your password..."
sudo -v

# Check for Homebrew
if ! command -v brew &>/dev/null; then
  echo "📦 Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "✅ Homebrew already installed"
fi

# Check for Python 3
if ! command -v python3 &>/dev/null; then
  echo "🐍 Installing Python 3..."
  brew install python
fi

# Check Python version
PY_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(echo "$PY_VERSION < 3.6" | bc) -eq 1 ]]; then
  echo "❌ Python 3.6 or higher is required (found $PY_VERSION)"
  exit 1
fi

# Check for Git
if ! command -v git &>/dev/null; then
  echo "🔧 Installing Git..."
  brew install git
fi

# Clone the repo
echo "📁 Cloning the repo..."
git clone https://github.com/Infernos1153/dj-music-cleaner.git ~/dj-music-cleaner
cd ~/dj-music-cleaner || { echo "❌ Failed to enter repo directory"; exit 1; }

# Install Python packages
echo "📦 Installing Python packages..."
pip3 install --upgrade pip setuptools
pip3 install -r requirements.txt

# Install external CLI tools
echo "🎧 Installing external tools (spotdl, yt-dlp)..."
brew install spotdl yt-dlp

# Install the CLI app
pip3 install .

echo "🎉 Done! You can now run 'dj-music-cleaner' from anywhere."
