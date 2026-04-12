from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# API端点
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        query = data.get('query', '')
        if not query:
            return jsonify({"error": "请输入问题"}), 400
        
        # 简单的响应
        return jsonify({"answer": f"你好！你问的是：{query}"})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)