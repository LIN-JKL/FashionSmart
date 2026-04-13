from flask import Flask, request, jsonify
import os
import sys

# 输出启动信息
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Environment variables: {os.environ}")

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    print("Health check endpoint called")
    return jsonify({"status": "ok"})

@app.route('/api/chat', methods=['POST'])
def chat():
    print("Chat endpoint called")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request data: {request.data}")
    return jsonify({"response": "这是一个测试响应"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)