from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

# 配置项
DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY')
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 初始化Flask应用
app = Flask(__name__)
# 明确配置CORS，允许所有来源
CORS(app, origins=["*"])

# 智能体回答函数
def fashion_agent_answer(query):
    try:
        print(f"Processing query: {query}")
        
        # 检查环境变量
        print(f"Environment variables: DASHSCOPE_API_KEY exists: {'DASHSCOPE_API_KEY' in os.environ}")
        
        # 尝试导入openai
        try:
            import openai
            print("OpenAI module imported successfully")
        except ImportError as e:
            print(f"Failed to import openai: {str(e)}")
            return f"❌ 回答失败：OpenAI模块未安装。错误信息：{str(e)}"
        
        # 检查API密钥
        if not DASHSCOPE_API_KEY:
            print("DASHSCOPE_API_KEY not set")
            return "❌ 回答失败：API密钥未配置"
        
        # 初始化OpenAI客户端
        try:
            client = openai.OpenAI(
                api_key=DASHSCOPE_API_KEY,
                base_url=DASHSCOPE_BASE_URL
            )
            print("OpenAI client initialized successfully")
        except Exception as e:
            print(f"Failed to initialize OpenAI client: {str(e)}")
            return f"❌ 回答失败：无法初始化客户端。错误信息：{str(e)}"
        
        # 构建消息
        messages = [
            {"role": "system", "content": "你是一名专业的服装电商运营智能体，回答要贴合电商场景，简洁实用。"},
            {"role": "user", "content": query}
        ]
        
        # 调用通义千问大模型生成回复（使用OpenAI兼容API）
        try:
            print("Making API call to OpenAI...")
            response = client.chat.completions.create(
                model="qwen-turbo",
                messages=messages,
                max_tokens=512,
                temperature=0.7
            )
            print("API call successful")
        except Exception as e:
            print(f"Failed to call OpenAI API: {str(e)}")
            return f"❌ 回答失败：API调用失败。错误信息：{str(e)}"
        
        # 提取回答内容
        try:
            answer = response.choices[0].message.content
            print(f"Received answer: {answer[:100]}...")  # 只打印前100个字符
        except Exception as e:
            print(f"Failed to extract answer: {str(e)}")
            return f"❌ 回答失败：无法提取回答内容。错误信息：{str(e)}"
        
        # 处理回答格式
        # 移除*、#、-等符号
        answer = answer.replace('*', '')
        answer = answer.replace('#', '')
        answer = answer.replace('-', '')
        # 确保适当的换行
        answer = answer.replace('\n\n', '<br><br>')
        answer = answer.replace('\n', '<br>')
        
        # 添加表情
        import random
        emojis = ['😊', '🌸', '👗', '👠', '👕', '👖', '👢', '👒', '🎀', '✨']
        # 在回答开头和中间随机添加表情
        answer_parts = answer.split('<br>')
        for i in range(len(answer_parts)):
            if answer_parts[i].strip():
                # 随机决定是否添加表情
                if random.random() > 0.7:
                    emoji = random.choice(emojis)
                    answer_parts[i] = f"{emoji} {answer_parts[i]}"
        # 在回答结尾添加表情
        emoji = random.choice(emojis)
        answer = '<br>'.join(answer_parts) + f" {emoji}"
        
        return answer
    except Exception as e:
        print(f"Error in fashion_agent_answer: {str(e)}")
        print(traceback.format_exc())
        return f"❌ 回答失败：{str(e)}"

# API端点
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