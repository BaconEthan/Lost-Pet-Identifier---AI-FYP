#!/bin/bash
# Installation script for Lost Pet Identifier

set -e

echo "=== Lost Pet Identifier Installation ==="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for Ollama
echo ""
echo "Checking for Ollama..."
if command -v ollama &> /dev/null; then
        echo "Ollama is installed"
    echo "Checking for llama2 model..."
    if ollama list | grep -q llama2; then
            echo "llama2 model found"
    else
        echo "WARNING: llama2 model not found. Run: ollama pull llama2"
    fi
else
    echo "WARNING: Ollama not found. Please install from https://ollama.ai"
    echo "  After installation, run: ollama pull llama2"
fi

# Create data directory
echo ""
echo "Creating data directory..."
mkdir -p data

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start using the system:"
echo "  1. Start Ollama: ollama serve"
echo "  2. Add found pets: python main.py add-found --help"
echo "  3. Search: python main.py search --help"
echo ""

