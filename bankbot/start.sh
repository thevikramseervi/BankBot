#!/bin/bash

echo "🚀 Starting BankBot - AI Banking Assistant"
echo "=========================================="

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    pkill -f "uvicorn main:app"
    pkill -f "npm run dev"
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup SIGINT SIGTERM

# Start FastAPI backend
echo "🔧 Starting FastAPI backend..."
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Create demo user
echo "👤 Creating demo user..."
cd backend
source venv/bin/activate
python create_demo_user.py
cd ..

# Start Next.js frontend
echo "🎨 Starting Next.js frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 8

# Check if frontend is running
if curl -s http://localhost:3000/ > /dev/null; then
    echo "✅ Frontend is running on http://localhost:3000"
else
    echo "❌ Frontend failed to start"
    exit 1
fi

echo ""
echo "🎉 BankBot is now running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🔐 Demo Login:"
echo "   Email: demo@bankbot.com"
echo "   Password: demo123"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for background processes
wait