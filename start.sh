#!/bin/bash

# Orato - AI Voice Processing Suite
# Quick start script

echo "🎤 Starting Orato - AI Voice Processing Suite"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads downloads

# Build and start the application
echo "🐳 Building and starting Orato..."
docker-compose up --build -d

# Wait for the application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost:5001/ &> /dev/null; then
    echo "✅ Orato is now running!"
    echo "🌐 Open your browser and go to: http://localhost:5001"
    echo ""
    echo "📋 Quick Commands:"
    echo "   Stop:    docker-compose down"
    echo "   Logs:    docker-compose logs -f"
    echo "   Restart: docker-compose restart"
    echo ""
    echo "🎉 Enjoy using Orato!"
else
    echo "❌ Failed to start Orato. Check the logs:"
    echo "   docker-compose logs"
    exit 1
fi
