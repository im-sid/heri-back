#!/bin/bash
# ============================================================
# Heri-Sci Backend Installation Script (Linux/macOS)
# ============================================================

echo ""
echo "============================================================"
echo "Heri-Sci Backend Installation"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1/5] Python detected"
python3 --version
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created successfully!"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo ""

# Upgrade pip
echo "[4/5] Upgrading pip..."
python -m pip install --upgrade pip
echo ""

# Install requirements
echo "[5/5] Installing dependencies..."
pip install -r requirements.txt
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "============================================================"
    echo "IMPORTANT: Please edit .env file and add your API keys!"
    echo "============================================================"
    echo ""
fi

# Create upload directories
mkdir -p uploads
mkdir -p processed

echo ""
echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Run: python app.py"
echo "3. Backend will start on http://localhost:5000"
echo ""
echo "To activate virtual environment later:"
echo "    source venv/bin/activate"
echo ""
