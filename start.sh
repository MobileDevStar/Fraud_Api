#!/usr/bin/env bash
bash fetch_model.sh

exec uvicorn src.api.main:app --host 0.0.0.0 --port $PORT