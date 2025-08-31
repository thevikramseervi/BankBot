#!/bin/bash

echo "🚀 Starting BankBot - AI Chatbot for Banking FAQs"
echo "=================================================="

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $DJANGO_PID $NEXT_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start Django backend
echo "🐍 Starting Django backend..."
cd backend
source venv/bin/activate
python manage.py runserver &
DJANGO_PID=$!
cd ..

# Wait a moment for Django to start
sleep 3

# Start Next.js frontend
echo "⚛️  Starting Next.js frontend..."
cd frontend
npm run dev &
NEXT_PID=$!
cd ..

echo "✅ Both servers are starting up..."
echo "🌐 Backend: http://localhost:8000"
echo "🎨 Frontend: http://localhost:3000"
echo "🤖 Admin: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for both processes
wait