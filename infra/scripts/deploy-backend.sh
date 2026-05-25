#!/bin/bash
set -e

SERVICE="edugenie-backend"
REGION="us-central1"
IMAGE="us-central1-docker.pkg.dev/${GCP_PROJECT_ID}/edugenie/backend:${SHORT_SHA}"

gcloud builds submit --config infra/cloudbuild.yaml

gcloud run deploy "$SERVICE" \
  --image="$IMAGE" \
  --region="$REGION" \
  --platform=managed \
  --allow-unauthenticated \
  --memory=2Gi \
  --cpu=2 \
  --min-instances=1 \
  --max-instances=100 \
  --concurrency=80

echo "Deployed $SERVICE to $REGION"
