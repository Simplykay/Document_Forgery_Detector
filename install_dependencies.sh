#!/bin/bash

# Function to check and install a package
install_if_missing() {
    PACKAGE=$1
    COMMAND=$2
    
    if command -v $COMMAND &> /dev/null; then
        echo "✅ $PACKAGE is already installed."
    else
        echo "⏳ $PACKAGE not found. Attempting to install..."
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            if command -v apt-get &> /dev/null; then
                sudo apt-get update && sudo apt-get install -y $PACKAGE
            else
                echo "❌ Unsupported Linux distribution. Please install $PACKAGE manually."
            fi
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            if command -v brew &> /dev/null; then
                brew install $PACKAGE
            else
                echo "❌ Homebrew not found. Please install $PACKAGE manually."
            fi
        elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            echo "ℹ️ Windows detected. Please install $PACKAGE using a package manager like Chocolatey or Scoop:"
            if [[ "$PACKAGE" == "poppler-utils" ]]; then
                echo "   choco install poppler"
            elif [[ "$PACKAGE" == "exiftool" ]]; then
                echo "   choco install exiftool"
            fi
        else
            echo "❌ Unknown OS. Please install $PACKAGE manually."
        fi
    fi
}

echo "🔍 Checking system dependencies..."

# Poppler-utils (provides pdftoppm)
install_if_missing "poppler-utils" "pdftoppm"

# ExifTool
install_if_missing "exiftool" "exiftool"

echo "✨ System dependency check complete!"
