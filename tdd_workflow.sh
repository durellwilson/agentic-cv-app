#!/bin/bash

echo "🧪 TDD Development Workflow"

# Watch for file changes and run tests
echo "Starting TDD watch mode..."
echo "Write tests first, then implement features!"

while true; do
    echo "Running tests..."
    pytest tests/ -v --tb=short
    
    echo "Watching for changes... (Ctrl+C to exit)"
    fswatch -1 app.py tests/ > /dev/null 2>&1
done
