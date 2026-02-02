#!/bin/bash

# Spike Dashboard Setup Script
# This script helps set up the Spike Dashboard with AI Alert Analysis

echo "========================================="
echo "🚨 Spike Dashboard Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found"
echo ""

# Create virtual environment (optional but recommended)
echo "Would you like to create a virtual environment? (recommended) [y/n]"
read -r create_venv

if [ "$create_venv" = "y" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "✅ Virtual environment created and activated"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Set up environment variables
if [ ! -f .env ]; then
    echo "Setting up environment variables..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your API credentials:"
    echo "   - SPIKE_API_KEY"
    echo "   - SPIKE_TEAM_ID"
    echo "   - ANTHROPIC_API_KEY"
    echo ""
    echo "Get your Spike credentials from: https://app.spike.sh/settings/api"
    echo "Get your Anthropic key from: https://console.anthropic.com/"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Check if .env is configured
echo "Checking if .env is configured..."
if grep -q "your_spike_api_key_here" .env; then
    echo "⚠️  Warning: .env file still contains placeholder values"
    echo "   Please edit .env and add your actual API credentials"
    echo ""
fi

# All done
echo "========================================="
echo "✅ Setup complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your API credentials"
echo "2. Run: streamlit run app.py"
echo "3. Open http://localhost:8501 in your browser"
echo ""
echo "For more info, see README.md"
echo ""

# Ask if they want to start the app
echo "Would you like to start the dashboard now? [y/n]"
read -r start_app

if [ "$start_app" = "y" ]; then
    echo ""
    echo "Starting Spike Dashboard..."
    streamlit run app.py
fi
