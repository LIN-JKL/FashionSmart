import http.server
import socketserver
import json
import os

PORT = int(os.environ.get('PORT', 5000))

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            # 不尝试读取请求体，直接返回响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps({"answer": "Hello from ultra simple HTTP server!"})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps({"status": "ok"})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()