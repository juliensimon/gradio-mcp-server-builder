#!/bin/bash

# Development setup script for gradio-mcp-server-builder

echo "Setting up development environment for gradio-mcp-server-builder..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Run pre-commit on all files
echo "Running pre-commit on all files..."
pre-commit run --all-files

echo "Development environment setup complete!"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
echo "To run pre-commit manually:"
echo "  pre-commit run --all-files"
echo ""
echo "To run tests:"
echo "  pytest"
