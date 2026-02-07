# Dockerfile for Habermolt backend deployment
# This Dockerfile is at the repository root to access both backend/ and habermas_machine/

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy habermas_machine first and install it
COPY habermas_machine /app/habermas_machine
RUN pip install -e /app/habermas_machine

# Copy backend requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend /app

# Expose port (Railway will set $PORT)
EXPOSE 8000

# Run migrations and start server
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
