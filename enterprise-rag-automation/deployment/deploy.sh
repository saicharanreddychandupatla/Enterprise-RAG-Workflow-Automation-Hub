#!/bin/bash

# Enterprise RAG Hub Deployment Script
echo "🚀 Deploying Enterprise RAG Hub to GCP Cloud Run..."

# Set variables
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="enterprise-rag-hub"
REGION="us-central1"

echo "📁 Project: $PROJECT_ID"
echo "🏷️ Service: $SERVICE_NAME"

# Build Docker image
echo "🐳 Building Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2

echo "✅ Deployment complete!"
echo "🌐 Your Enterprise RAG Hub is now live on Cloud Run"
