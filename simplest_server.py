from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import os

# 打印Python版本和环境信息
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Environment variables: {dict(os.environ)}")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(f"Received POST request to: {self.path}")
        print(f"Headers: {dict(self.headers)}")
        
        # 获取请求体长度
        content_length = int(self.headers['Content-Length'])
        # 读取请求体
        post_data = self.rfile.read(content_length)
        print(f"Raw POST data: {post_data}")
        
        # 发送响应
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 简单的响应
        response = {
            "response": "这是一个最简单的响应"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        if self.path == '/api/health':
            print(f"Received GET request to: {self.path}")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "ok"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://localhost:{port}/")
    print(f"Available endpoints:")
    print(f"  GET  /api/health")
    print(f"  POST /api/chat")
    httpd.serve_forever()

if __name__ == '__main__':
    run()