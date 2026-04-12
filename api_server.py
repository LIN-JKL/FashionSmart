from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# API端点
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # 打印请求信息
        print(f"Request method: {request.method}")
        print(f"Request path: {request.path}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request data: {request.data}")
        
        data = request.json
        print(f"Request json: {data}")
        
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        
        query = data.get('query', '')
        if not query:
            return jsonify({"error": "请输入问题"}), 400
        
        # 简单的响应
        response = jsonify({"answer": f"你好！你问的是：{query}"})
        print(f"Response: {response.data}")
        return response
    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()
        print(f"Error in chat endpoint: {error_message}")
        print(f"Traceback: {error_traceback}")
        return jsonify({"error": f"服务器内部错误: {error_message}"}), 500

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)