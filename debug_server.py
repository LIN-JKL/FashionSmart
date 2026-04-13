import http.server
import socketserver
import os
import sys

# 输出启动信息
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Environment variables: {os.environ}")

PORT = int(os.environ.get('PORT', 8000))
print(f"Starting server on port {PORT}")

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"GET request received for path: {self.path}")
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            print("Health check response sent")
        else:
            super().do_GET()
    
    def do_POST(self):
        print(f"POST request received for path: {self.path}")
        if self.path == '/api/chat':
            # 尝试读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            print(f"Content length: {content_length}")
            if content_length > 0:
                body = self.rfile.read(content_length)
                print(f"Request body: {body}")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"response": "这是一个测试响应"}')
            print("Chat response sent")
        else:
            self.send_response(404)
            self.end_headers()
            print(f"404 response sent for path: {self.path}")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()