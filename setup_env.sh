#!/bin/bash
echo "Creating virtual environment..."
python -m venv venv

echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete!"
