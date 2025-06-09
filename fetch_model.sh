#!/usr/bin/env bash
#
# Download the model from Google Drive if not already present.

# Replace <YOUR_GOOGLE_DRIVE_FILE_ID> with your actual file ID.
# https://drive.google.com/file/d/13ck3HS9E2tMrFdTkZrtzveyZq2q60xLd/view?usp=sharing

MODEL_ID="13ck3HS9E2tMrFdTkZrtzveyZq2q60xLd"
MODEL_URL="https://drive.google.com/uc?export=download&id=${MODEL_ID}"
TARGET_PATH="models/fraud_detector.h5"

# Ensure the models directory exists
mkdir -p models

# Only fetch if it doesn't already exist
if [ ! -f "$TARGET_PATH" ]; then
  echo "Fetching fraud_detector.h5 from Google Drive via gdown..."
  # Install gdown (in case it's not on PATH)
  pip install --no-cache-dir gdown

  # Use gdown to download by ID
  gdown "https://drive.google.com/uc?id=${MODEL_ID}" -O "$TARGET_PATH"
  if [ $? -ne 0 ]; then
    echo "❌ gdown failed to download model."
    exit 1
  fi
  echo "✅ Model downloaded to $TARGET_PATH"
else
  echo "✅ Model already present at $TARGET_PATH"
fi