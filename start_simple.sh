#!/bin/bash

# Simple TasteTrailOps Startup Script
# This version uses the simplified API without import issues

echo "🍽️  Starting TasteTrailOps (Simple Version)"
echo "=========================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# Install basic requirements
print_info "Installing dependencies..."
pip install fastapi uvicorn python-multipart >/dev/null 2>&1
print_success "Dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cat > .env << EOF
QLOO_API_KEY=your_qloo_api_key_here
ENVIRONMENT=development
EOF
    print_info ".env file created"
fi

# Stop any existing processes
if [ -f "api.pid" ]; then
    kill $(cat api.pid) 2>/dev/null
    rm api.pid
fi

if [ -f "frontend.pid" ]; then
    kill $(cat frontend.pid) 2>/dev/null
    rm frontend.pid
fi

# Start the API
print_info "Starting API server..."
source .env
nohup python3 api_simple.py > api.log 2>&1 &
API_PID=$!
echo $API_PID > api.pid

# Wait for API to start
sleep 3

# Check API health
API_HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
if echo "$API_HEALTH" | grep -q "healthy"; then
    print_success "API server running on http://localhost:8000 (PID: $API_PID)"
else
    print_warning "API server might still be starting up"
fi

# Start the frontend
print_info "Starting frontend server..."
cd frontend
nohup python3 server.py > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../frontend.pid
cd ..

# Wait for frontend to start
sleep 2

# Check frontend
if curl -s -I http://localhost:3000 >/dev/null 2>&1; then
    print_success "Frontend server running on http://localhost:3000 (PID: $FRONTEND_PID)"
else
    print_warning "Frontend server might still be starting up"
fi

echo ""
print_success "🎉 TasteTrailOps is running!"
echo ""
print_info "📱 Access the application:"
echo "   • Frontend: http://localhost:3000"
echo "   • API Docs: http://localhost:8000/docs"
echo "   • API Health: http://localhost:8000/health"
echo ""
print_info "📝 Management commands:"
echo "   • View logs: tail -f api.log && tail -f frontend.log"
echo "   • Stop services: ./stop_local.sh"
echo ""
print_info "🧪 Test the API:"
echo "   curl http://localhost:8000/health"
echo ""

# Create updated stop script
cat > stop_local.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping TasteTrailOps services..."

if [ -f "api.pid" ]; then
    kill $(cat api.pid) 2>/dev/null
    rm api.pid
    echo "✅ API server stopped"
fi

if [ -f "frontend.pid" ]; then
    kill $(cat frontend.pid) 2>/dev/null
    rm frontend.pid
    echo "✅ Frontend server stopped"
fi

echo "🎉 All services stopped!"
EOF

chmod +x stop_local.sh

print_success "Ready to use! Open http://localhost:3000 in your browser"
