# Multi-stage build for Healthcare Assistant App
FROM node:18-alpine AS node-base

# Python stage
FROM python:3.11-slim AS python-base
WORKDIR /app
COPY ai_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend stage
FROM node-base AS backend
WORKDIR /app/server
COPY server/package*.json ./
RUN npm ci --only=production
COPY server/ .

# Frontend stage
FROM node-base AS frontend
WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci
COPY client/ .
RUN npm run build

# Production stage
FROM python:3.11-slim AS production
WORKDIR /app

# Install Node.js
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY --from=python-base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-base /usr/local/bin /usr/local/bin

# Copy backend
COPY --from=backend /app /app/server
COPY --from=backend /usr/local/lib/node_modules /usr/local/lib/node_modules

# Copy frontend build
COPY --from=frontend /app/build /app/client/build

# Copy AI service
COPY ai_service/ /app/ai_service/

# Copy startup script
COPY start_app.py /app/
COPY docker-entrypoint.sh /app/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 3000 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"] 