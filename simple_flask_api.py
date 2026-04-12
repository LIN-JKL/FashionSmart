from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

app = Flask(__name__)
CORS(app)  # 启用CORS

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # 记录请求信息
        print(f"Received POST request to /api/chat")
        print(f"Content-Type: {request.content_type}")
        print(f"Request data: {request.data}")
        
        # 尝试获取JSON数据
        data = request.get_json(force=True)
        print(f"Parsed JSON: {data}")
        
        if not data or 'query' not in data:
            print("Missing query parameter")
            return jsonify({"error": "Missing query parameter"}), 400
        
        print(f"Query: {data['query']}")
        return jsonify({"response": "这是一个测试响应"})
    except Exception as e:
        # 记录详细错误信息
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)