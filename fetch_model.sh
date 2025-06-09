#!/usr/bin/env bash
#
# Download the model from GitHub Releases if missing.

REPO="MobileDevStar/Fraud_Api"
TAG="v1.0-model"
MODEL_FILE="fraud_detector.h5"
URL="https://github.com/${REPO}/releases/download/${TAG}/${MODEL_FILE}"
TARGET="models/${MODEL_FILE}"

mkdir -p models

if [ ! -f "$TARGET" ]; then
  echo "Downloading ${MODEL_FILE} from GitHub Releases..."
  curl -L -o "$TARGET" "$URL"
  if [ $? -ne 0 ]; then
    echo "❌ Failed to download model from $URL"
    exit 1
  fi
  echo "✅ Model downloaded to $TARGET"
else
  echo "✅ Model already exists at $TARGET"
fi
