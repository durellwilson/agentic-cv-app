#!/bin/bash

echo "🚀 Deploying Agentic CV App..."

# Run tests first
echo "Running tests..."
pytest tests/ -v

if [ $? -eq 0 ]; then
    echo "✅ Tests passed!"
    
    # Build Docker image
    echo "Building Docker image..."
    docker build -t agentic-cv-app .
    
    # Deploy options
    echo "Choose deployment option:"
    echo "1. Railway (recommended)"
    echo "2. Docker locally"
    echo "3. Heroku"
    
    read -p "Enter choice (1-3): " choice
    
    case $choice in
        1)
            echo "Deploy to Railway:"
            echo "1. Install Railway CLI: npm install -g @railway/cli"
            echo "2. Login: railway login"
            echo "3. Deploy: railway up"
            ;;
        2)
            echo "Running locally with Docker..."
            docker run -p 5000:5000 agentic-cv-app
            ;;
        3)
            echo "Deploy to Heroku:"
            echo "1. Install Heroku CLI"
            echo "2. heroku create your-app-name"
            echo "3. git push heroku main"
            ;;
    esac
else
    echo "❌ Tests failed! Fix issues before deploying."
    exit 1
fi
