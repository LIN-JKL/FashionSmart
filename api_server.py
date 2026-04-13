from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

app = Flask(__name__)
CORS(app)

# 根路径
@app.route('/')
def home():
    try:
        return jsonify({"message": "Hello World"})
    except Exception as e:
        print(f"Error in home: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

# 健康检查
@app.route('/api/health')
def health():
    try:
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Error in health: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

# 聊天端点
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # 打印请求信息
        print(f"Request method: {request.method}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request content type: {request.content_type}")
        
        # 尝试获取JSON数据
        if request.is_json:
            data = request.get_json()
            print(f"Request JSON data: {data}")
            query = data.get('query', '')
            return jsonify({"answer": f"收到：{query}"})
        else:
            # 如果不是JSON，返回错误
            print("Request is not JSON")
            print(f"Request data: {request.data}")
            return jsonify({"error": "Request must be JSON"}), 400
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)