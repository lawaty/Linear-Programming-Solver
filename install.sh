#!/bin/bash

echo "🚀 Starting installation..."

# Exit immediately if a command fails
set -e

# Install Electron dependencies
echo "📦 Installing Electron dependencies..."
npm install

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd server

if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "✅ Virtual environment created."
else
  echo "⚡ Virtual environment already exists, skipping creation."
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Installation complete!"
