#!/bin/bash

# Prompt for password once
echo "🔐 Admin privileges are needed. Enter your password if prompted:"
sudo -v

# Prompt for GitHub credentials
read -p "Enter your GitHub username: " GITHUB_USER
read -s -p "Enter your GitHub password or token: " GITHUB_PASS
echo ""

# Check and install Homebrew
if ! command -v brew &>/dev/null; then
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew already installed"
fi

# Check and install Python 3
if ! command -v python3 &>/dev/null; then
    echo "🐍 Installing Python 3..."
    brew install python
else
    echo "✅ Python 3 already installed"
fi

# Check Python version
PY_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(echo "$PY_VERSION < 3.6" | bc) -eq 1 ]]; then
    echo "❌ Python 3.6+ is required. You have $PY_VERSION"
    exit 1
fi

# Check and install Git
if ! command -v git &>/dev/null; then
    echo "🔧 Installing Git..."
    brew install git
else
    echo "✅ Git already installed"
fi

# Clone the repo
echo "📁 Cloning the repo..."
git clone https://"$GITHUB_USER":"$GITHUB_PASS"@github.com/Infernos1153/dj-music-cleaner.git ~/dj-music-cleaner
cd ~/dj-music-cleaner || exit 1

# Install pip packages
echo "📦 Installing Python packages..."
pip3 install --upgrade pip setuptools
pip3 install -r requirements.txt

# Install external tools
echo "🎧 Installing spotdl and yt-dlp..."
brew install spotdl yt-dlp

# Install the CLI app
echo "⚙️ Installing the app CLI..."
pip3 install .

echo "🎉 Done! You can now run 'dj-music-cleaner' from anywhere."
