from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # 启用CORS

@app.route('/api/chat', methods=['POST'])
def chat():
    # 不尝试读取请求体，直接返回响应
    return jsonify({"answer": "Hello from Flask API!"})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)