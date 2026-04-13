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
        # 处理所有GET请求，返回相同的响应
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"message": "Hello from the server!"}')
        print("Response sent")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()