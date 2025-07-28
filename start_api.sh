#!/bin/bash
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
