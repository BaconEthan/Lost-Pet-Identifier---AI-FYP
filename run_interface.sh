#!/bin/bash
# Script to run the web interface

# Activate virtual environment
source venv/bin/activate

# Set OpenMP environment variable (macOS)
export KMP_DUPLICATE_LIB_OK=TRUE

# Install streamlit if not already installed
pip install -q streamlit

# Run the Streamlit app
echo "Starting Lost Pet Identifier web interface..."
echo "The interface will open in your browser automatically."
echo "Press Ctrl+C to stop the server."
echo ""

streamlit run app.py

