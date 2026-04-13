from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback
import sys

# 初始化Flask应用
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 明确允许所有来源

# 打印环境信息
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Environment variables: {dict(os.environ)}")

# API端点
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        query = data.get('query', '')
        if not query:
            return jsonify({"error": "请输入问题"}), 400
        
        # 简单的响应
        return jsonify({"answer": f"你好！你问的是：{query}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 根路径路由
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "FashionSmart API Server",
        "endpoints": {
            "/api/health": "GET - Health check",
            "/api/chat": "POST - Chat endpoint"
        }
    })

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)