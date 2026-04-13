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
    try:
        print(f"Request method: {request.method}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request content type: {request.content_type}")
        
        # 先尝试获取原始数据
        raw_data = request.get_data(as_text=True)
        print(f"Raw request data: {raw_data}")
        
        # 再尝试解析JSON
        data = request.get_json()
        print(f"Parsed JSON data: {data}")
        
        query = data.get('query', '')
        print(f"Received query: {query}")
        
        # 模拟响应，不调用任何外部API
        response = {
            "response": f"这是一个模拟响应，你询问的是：{query}"
        }
        
        print(f"Response: {response}")
        return jsonify(response)
    except Exception as e:
        error_message = f"Error in /api/chat: {str(e)}"
        print(error_message)
        import traceback
        traceback.print_exc()
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)