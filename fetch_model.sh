#!/usr/bin/env bash
set -e

MODEL_ID="13ck3HS9E2tMrFdTkZrtzveyZq2q60xLd"
TARGET="models/fraud_detector.h5"

mkdir -p models

if [ ! -f "$TARGET" ]; then
  echo "Downloading model from Google Drive..."
  gdown --id "$MODEL_ID" -O "$TARGET"
  echo "✅ Downloaded to $TARGET"
else
  echo "✅ Model already present"
fi
