#!/bin/bash

echo "🤖 Setting up Agentic Computer Vision Flask App..."

# Create virtual environment
python -m venv cv_env
source cv_env/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "✅ Setup complete!"
echo "To run the app:"
echo "1. source cv_env/bin/activate"
echo "2. python app.py"
echo "3. Open http://localhost:5000"
