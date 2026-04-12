import http.server
import socketserver
import json
import os
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 5000))

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            logger.info(f'Received POST request to {self.path}')
            logger.info(f'Headers: {dict(self.headers)}')
            
            if self.path == '/api/chat':
                content_length = int(self.headers.get('Content-Length', 0))
                logger.info(f'Content length: {content_length}')
                
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    logger.info(f'Post data: {post_data}')
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = json.dumps({"answer": "Hello from logging HTTP server!"})
                logger.info(f'Response: {response}')
                self.wfile.write(response.encode('utf-8'))
            else:
                logger.info(f'404 Not Found: {self.path}')
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            logger.error(f'Error: {e}')
            self.send_response(500)
            self.end_headers()
    
    def do_GET(self):
        try:
            logger.info(f'Received GET request to {self.path}')
            
            if self.path == '/api/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = json.dumps({"status": "ok"})
                logger.info(f'Response: {response}')
                self.wfile.write(response.encode('utf-8'))
            else:
                logger.info(f'404 Not Found: {self.path}')
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            logger.error(f'Error: {e}')
            self.send_response(500)
            self.end_headers()

if __name__ == '__main__':
    logger.info(f'Starting server on port {PORT}')
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        logger.info(f'Server running on port {PORT}')
        httpd.serve_forever()