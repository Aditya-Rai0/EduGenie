#!/bin/bash
set -e

SERVICE="edugenie-frontend"
REGION="us-central1"
IMAGE="us-central1-docker.pkg.dev/${GCP_PROJECT_ID}/edugenie/frontend:${SHORT_SHA}"

gcloud run deploy "$SERVICE" \
  --image="$IMAGE" \
  --region="$REGION" \
  --platform=managed \
  --allow-unauthenticated

echo "Deployed $SERVICE to $REGION"
