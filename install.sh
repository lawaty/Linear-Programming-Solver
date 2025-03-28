#!/bin/bash

echo "🚀 Starting installation..."

# Exit immediately if a command fails
set -e

# Install Electron dependencies
echo "📦 Installing Electron dependencies..."
npm install

# Install electron-builder as a dev dependency (project-local)
if [ ! -d "node_modules/electron-builder" ]; then
  echo "🔧 Installing electron-builder locally..."
  npm install --save-dev electron-builder
else
  echo "⚡ electron-builder is already installed."
fi

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd server

if [ ! -d "venv" ]; then
  echo "✅ Virtual environment does not exist. Creating one..."
  
  # Check OS type
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    python -m venv venv  # Windows
  else
    python3 -m venv venv  # Linux/macOS
  fi
else
  echo "⚡ Virtual environment already exists, skipping creation."
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  source venv/Scripts/activate  # Windows
else
  source venv/bin/activate  # Linux/macOS
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Installation complete!"
