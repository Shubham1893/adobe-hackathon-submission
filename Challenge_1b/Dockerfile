# Challenge 1b ROBUST Dockerfile
FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

# Install dependencies first
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Download and save the model INSIDE the image during build
COPY download_model.py .
RUN python download_model.py

# Copy the rest of the application
COPY analyzer.py .

# Default command
CMD ["echo", "Container ready for Round 1B analysis."]