#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting OPEA setup..."

# Check if virtual environment exists and activate it
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install OPEA Comps and Streamlit
echo "📚 Installing required packages..."
pip install opea-comps streamlit

# Create models directory if it doesn't exist
echo "📥 Setting up model directory..."
mkdir -p models

# Download language models
echo "🔄 Downloading language models (this may take some time)..."
# Download German-English translation model
if [ ! -f "models/german_english_model.tar.gz" ]; then
    echo "Downloading German-English translation model..."
    curl -L https://huggingface.co/Helsinki-NLP/opus-mt-de-en/resolve/main/pytorch_model.bin -o models/german_english_model.tar.gz
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build and start the containers
echo "🏗️ Building Docker images..."
docker-compose build

echo "🐳 Starting microservices..."
docker-compose up -d

# Wait for services to initialize
echo "⏳ Waiting for services to initialize..."
echo "This will take approximately 30 seconds..."

# Progress bar simulation
for i in {1..30}; do
    echo -n "."
    sleep 1
done
echo ""

# Check if all services are healthy
echo "🔍 Checking service health..."
if ! curl -s http://localhost:9000/health > /dev/null; then
    echo "❌ LLM service is not responding"
    exit 1
fi

if ! curl -s http://localhost:6000/health > /dev/null; then
    echo "❌ Embedding service is not responding"
    exit 1
fi

if ! curl -s http://localhost:7001/health > /dev/null; then
    echo "❌ TTS service is not responding"
    exit 1
fi

echo "✅ All services are healthy!"

# Start the Streamlit app
echo "🌟 Starting Streamlit app..."
streamlit run app.py

# Cleanup function
cleanup() {
    echo "🛑 Shutting down services..."
    docker-compose down
    deactivate
    echo "👋 Goodbye!"
}

# Register cleanup function to run on script exit
trap cleanup EXIT 