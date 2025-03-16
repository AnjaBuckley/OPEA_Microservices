# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create models directory
RUN mkdir -p /models

# Set environment variables
ENV MODEL_PATH=/models/german_english_model

# Expose the port
EXPOSE 9000

# Run the service
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "9000"] 