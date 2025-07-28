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
