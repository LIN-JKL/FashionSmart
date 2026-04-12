import http.server
import socketserver
import json
import os

PORT = int(os.environ.get('PORT', 5000))

class Handler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def do_POST(self):
        try:
            if self.path == '/api/chat':
                self._set_headers()
                response = json.dumps({"answer": "Hello from simple POST API!"})
                self.wfile.write(response.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            # 即使有错误，也返回200 OK
            self._set_headers()
            response = json.dumps({"answer": "Error occurred"})
            self.wfile.write(response.encode('utf-8'))
    
    def do_GET(self):
        if self.path == '/api/health':
            self._set_headers()
            response = json.dumps({"status": "ok"})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()