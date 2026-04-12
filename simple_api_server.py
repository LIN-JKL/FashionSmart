from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

app = Flask(__name__)
# 明确配置CORS，允许所有来源
CORS(app, origins=["*"])

# 智能体回答函数
def fashion_agent_answer(query):
    try:
        print(f"Processing query: {query}")
        # 简单返回固定响应，排除API调用问题
        return f"您好！这是一个测试响应。您的查询是：{query}"
    except Exception as e:
        print(f"Error in fashion_agent_answer: {str(e)}")
        print(traceback.format_exc())
        return f"抱歉，我暂时无法回答您的问题。错误信息：{str(e)}"

# 聊天接口
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        print("Chat endpoint called")
        # 获取请求数据
        data = request.get_json()
        print(f"Received data: {data}")
        
        if not data or 'query' not in data:
            print("Missing query parameter")
            return jsonify({"error": "请输入问题"}), 400
        
        # 获取用户查询
        query = data['query']
        print(f"Processing query: {query}")
        
        # 调用时尚顾问函数
        answer = fashion_agent_answer(query)
        print(f"Generated answer: {answer[:100]}...")
        
        # 返回回答
        return jsonify({"answer": answer}), 200
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        print("Health check endpoint called")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error in health_check: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    print(f"Flask version: {Flask.__version__}")
    app.run(host='0.0.0.0', port=5000, debug=True)