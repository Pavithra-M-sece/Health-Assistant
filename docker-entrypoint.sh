#!/bin/bash
set -e

echo "🚀 Healthcare Assistant App - Docker Container"
echo "=============================================="

# Function to handle shutdown
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $AI_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Start backend
echo "🟢 Starting Backend..."
cd /app/server
node index.js &
BACKEND_PID=$!

# Start AI service
echo "🟢 Starting AI Service..."
cd /app/ai_service
python new_backend.py &
AI_PID=$!

# Start frontend (serve static files)
echo "🟢 Starting Frontend..."
cd /app/client
npx serve -s build -l 3000 &
FRONTEND_PID=$!

echo "✅ All services started!"
echo "📍 Access Points:"
echo "   • Frontend:  http://localhost:3000"
echo "   • Backend:   http://localhost:5000"
echo "   • AI Service: http://localhost:5000"

# Wait for all processes
wait 