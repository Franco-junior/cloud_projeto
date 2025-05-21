#!/bin/bash

# Note: Replace 'crowdi' with your Docker Hub username

# Build the image
echo "Building Docker image..."
docker build -t crowdi/insper-cloud-projeto:latest ./api

# Log in to Docker Hub
echo "Logging in to Docker Hub..."
docker login

# Push the image to Docker Hub
echo "Pushing image to Docker Hub..."
docker push crowdi/insper-cloud-projeto:latest

echo "Image published successfully to Docker Hub!"
echo "Your image is now available at: crowdi/insper-cloud-projeto:latest" 