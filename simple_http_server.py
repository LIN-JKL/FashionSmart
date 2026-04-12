import http.server
import socketserver
import json
import os

PORT = int(os.environ.get('PORT', 5000))

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = json.dumps({"answer": "Hello from simple HTTP server!"})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = json.dumps({"status": "ok"})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print(f'Server running on port {PORT}')
    httpd.serve_forever()