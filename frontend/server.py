#!/usr/bin/env python3
"""
Simple HTTP server to serve the TasteTrailOps frontend
Run with: python3 server.py
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Configuration
PORT = 3000
DIRECTORY = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers for API calls
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()
    
    def guess_type(self, path):
        # Ensure proper MIME types
        result = super().guess_type(path)
        if result is None:
            mimetype, encoding = None, None
        elif isinstance(result, tuple):
            mimetype, encoding = result
        else:
            mimetype, encoding = result, None
            
        if path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.html'):
            return 'text/html'
        return mimetype

def main():
    # Change to the frontend directory
    os.chdir(DIRECTORY)
    
    print(f"🚀 Starting TasteTrailOps Frontend Server")
    print(f"📁 Serving directory: {DIRECTORY}")
    print(f"🌐 Server running at: http://localhost:{PORT}")
    print(f"📱 Access the app at: http://localhost:{PORT}/index.html")
    print(f"🔗 API should be running at: http://localhost:8000")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"✅ Server successfully started on port {PORT}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: Port {PORT} is already in use")
            print(f"💡 Try running on a different port or kill the existing process")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
