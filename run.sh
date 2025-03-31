#!/bin/sh

echo "📦 Running Alembic migrations..."
python -m alembic upgrade head

echo "🚀 Starting FastAPI app on http://localhost:8000 ..."
exec uvicorn src.main:app