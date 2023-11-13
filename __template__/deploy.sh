#!/bin/bash

gcloud functions deploy sample \
  --region asia-northeast1 \
  --runtime python310 \
  --memory 256MB \
  --timeout 540s \
  --entry-point main \
  --trigger-topic sample \
  --env-vars-file .env.prod.yaml