#!/bin/bash

echo "================================================"
echo "   📊 DataBoard - Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Create virtual environment (optional)
read -p "Create virtual environment? (recommended) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment activated"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/uploads
mkdir -p data/datasets
mkdir -p data/dashboards
mkdir -p static
echo "✓ Directories created"
echo ""

echo "================================================"
echo "   ✅ Setup Complete!"
echo "================================================"
echo ""
echo "To start the server:"
echo "  python app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:5000"
echo ""
echo "Default credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "================================================"
