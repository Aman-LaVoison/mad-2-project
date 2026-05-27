#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- Starting Environment Setup ---"

# 1. Ensure Python 3.11 is installed (deadsnakes PPA)
echo "Installing Python 3.11..."
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv -y

# 2. Clean up old venv
if [ -d "venv" ]; then
    echo "Removing old venv..."
    rm -rf venv
fi

# 3. Create fresh venv with Python 3.11
echo "Creating new virtual environment..."
python3.11 -m venv venv

# 4. Activate venv
source venv/bin/activate

# 5. Upgrade pip
pip install --upgrade pip

# 6. Install dependencies
echo "Installing dependencies..."
# We explicitly install setuptools < 66.0.0 to satisfy older passlib requirements
pip install "setuptools<66.0.0"
pip install -r requirements.txt

# Final output
echo "--- Setup Complete! ---"
echo "To activate your environment, run: source venv/bin/activate"
echo "Then run your app with: python run.py"