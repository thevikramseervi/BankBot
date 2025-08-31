#!/bin/bash

echo "🚀 Starting BankBot Application..."
echo "=================================="

# Function to cleanup background processes
cleanup() {
    echo "🛑 Stopping servers..."
    pkill -f "python manage.py runserver"
    pkill -f "npm run dev"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Start Django Backend
echo "📡 Starting Django Backend..."
cd backend
source venv/bin/activate
python manage.py runserver 127.0.0.1:8000 &
DJANGO_PID=$!
echo "✅ Django Backend started (PID: $DJANGO_PID)"

# Wait a moment for Django to start
sleep 3

# Start Next.js Frontend
echo "🌐 Starting Next.js Frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Next.js Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "🎉 BankBot is starting up!"
echo "=================================="
echo "🌐 Frontend: http://localhost:3000"
echo "📡 Backend:  http://localhost:8000"
echo "🔧 Admin:    http://localhost:8000/admin"
echo ""
echo "📱 Demo Accounts:"
echo "   Username: john_doe | Password: password123"
echo "   Username: jane_smith | Password: password123"
echo ""
echo "⏹️  Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait $DJANGO_PID $FRONTEND_PID