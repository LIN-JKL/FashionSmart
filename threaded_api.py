import http.server
import socketserver
import json
import os

PORT = int(os.environ.get('PORT', 5000))

class Handler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        # 处理CORS预检请求
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            if self.path == '/api/chat':
                self._set_headers()
                # 即使不读取请求体，也确保正确处理
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    # 读取但不处理请求体
                    self.rfile.read(content_length)
                response = json.dumps({"answer": "Hello from threaded API!"})
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
    # 使用ThreadingTCPServer以支持并发请求
    with socketserver.ThreadingTCPServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()