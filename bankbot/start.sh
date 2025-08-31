#!/bin/bash

# 🏦 BankBot - Perfect AI Banking Assistant
# Zero configuration needed - works out of the box!

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

print_success() {
    echo -e "${GREEN}🎉${NC} $1"
}

# Function to cleanup on exit
cleanup() {
    echo ""
    print_warning "Shutting down BankBot..."
    
    # Kill background processes
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Kill any remaining processes
    pkill -f "uvicorn main:app" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    
    print_success "BankBot stopped successfully!"
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup SIGINT SIGTERM

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ and try again."
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm and try again."
        exit 1
    fi
    
    print_status "All prerequisites are satisfied!"
}

# Setup backend
setup_backend() {
    print_info "Setting up FastAPI backend..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_warning "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_info "Installing Python dependencies..."
    pip install -q fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] passlib[bcrypt] python-multipart email-validator
    
    print_status "Backend setup completed!"
    cd ..
}

# Setup frontend
setup_frontend() {
    print_info "Setting up Next.js frontend..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_warning "Installing Node.js dependencies..."
        npm install -q
    fi
    
    print_status "Frontend setup completed!"
    cd ..
}

# Start backend
start_backend() {
    print_info "Starting FastAPI backend..."
    
    cd backend
    source venv/bin/activate
    
    # Start backend in background
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
    BACKEND_PID=$!
    
    cd ..
    
    # Wait for backend to start
    print_info "Waiting for backend to start..."
    sleep 5
    
    # Check if backend is running
    if curl -s http://localhost:8000/ > /dev/null; then
        print_status "Backend is running on http://localhost:8000"
    else
        print_error "Backend failed to start. Check backend.log for details."
        exit 1
    fi
}

# Start frontend
start_frontend() {
    print_info "Starting Next.js frontend..."
    
    cd frontend
    
    # Start frontend in background
    npm run dev > frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    cd ..
    
    # Wait for frontend to start
    print_info "Waiting for frontend to start..."
    sleep 10
    
    # Check if frontend is running
    if curl -s http://localhost:3000/ > /dev/null; then
        print_status "Frontend is running on http://localhost:3000"
    else
        print_error "Frontend failed to start. Check frontend.log for details."
        exit 1
    fi
}

# Display startup information
display_info() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🏦 BankBot is Running! 🏦                ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                                                              ║"
    echo "║  📱 Frontend: http://localhost:3000                        ║"
    echo "║  🔧 Backend:  http://localhost:8000                        ║"
    echo "║  📚 API Docs: http://localhost:8000/docs                   ║"
    echo "║  🔍 Alt Docs: http://localhost:8000/redoc                  ║"
    echo "║  💚 Health:   http://localhost:8000/health                 ║"
    echo "║                                                              ║"
    echo "║  🔐 Demo Login:                                             ║"
    echo "║     Email: demo@bankbot.com                                 ║"
    echo "║     Password: demo123                                       ║"
    echo "║                                                              ║"
    echo "║  🚀 Features:                                               ║"
    echo "║     • AI-powered banking chatbot                           ║"
    echo "║     • Secure authentication                                 ║"
    echo "║     • Account management                                    ║"
    echo "║     • Transaction tracking                                  ║"
    echo "║     • Beautiful modern UI                                   ║"
    echo "║                                                              ║"
    echo "║  Press Ctrl+C to stop all servers                          ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

# Main execution
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                🚀 Starting BankBot... 🚀                   ║"
    echo "║                                                              ║"
    echo "║  Perfect AI-powered banking assistant                       ║"
    echo "║  Zero configuration needed - works out of the box!          ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Setup components
    setup_backend
    setup_frontend
    
    # Start services
    start_backend
    start_frontend
    
    # Display information
    display_info
    
    # Wait for background processes
    wait
}

# Run main function
main