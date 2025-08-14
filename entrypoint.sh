#!/bin/sh
set -e

echo "Running alembic migrations..."
alembic upgrade head

echo "Seeding test data..."
python -m src.seed

echo "Starting FastAPI app..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
