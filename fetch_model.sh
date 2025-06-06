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

# If the model file is missing, download it:
if [ ! -f "$TARGET_PATH" ]; then
  echo "Downloading fraud_detector.h5 from Google Drive..."
  # Use curl with cookie handling to bypass Drive's warning page if file is large
  CONFIRM=$(curl -sc /tmp/gcookie "https://drive.google.com/uc?export=download&id=${MODEL_ID}" | \
            grep -o 'confirm=[^&]*' | sed 's/confirm=//')
  curl -Lb /tmp/gcookie "https://drive.google.com/uc?export=download&confirm=${CONFIRM}&id=${MODEL_ID}" -o "$TARGET_PATH"

  if [ $? -ne 0 ]; then
    echo "Error: failed to download model from Google Drive"
    exit 1
  fi
  echo "Model downloaded to $TARGET_PATH"
else
  echo "Model already exists at $TARGET_PATH"
fi
