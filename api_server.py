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
        # 打印请求信息
        print(f"=== Request received ===")
        print(f"Request method: {request.method}")
        print(f"Request path: {request.path}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Content-Type: {request.content_type}")
        
        # 尝试不同的方式获取数据
        try:
            data = request.json
            print(f"Request json: {data}")
        except Exception as json_error:
            print(f"JSON parsing error: {json_error}")
            data = None
        
        # 尝试获取原始数据
        if data is None:
            try:
                raw_data = request.get_data(as_text=True)
                print(f"Raw data: {raw_data}")
            except Exception as raw_error:
                print(f"Error getting raw data: {raw_error}")
            return jsonify({"error": "Invalid JSON"}), 400
        
        query = data.get('query', '')
        print(f"Extracted query: '{query}'")
        
        if not query:
            return jsonify({"error": "请输入问题"}), 400
        
        # 简单的响应
        response_data = {"answer": f"你好！你问的是：{query}"}
        print(f"Response data: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()
        print(f"=== Error in chat endpoint ===")
        print(f"Error message: {error_message}")
        print(f"Traceback: {error_traceback}")
        return jsonify({"error": f"服务器内部错误: {error_message}"}), 500

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)