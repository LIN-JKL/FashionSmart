from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# 配置项
DASHSCOPE_API_KEY = "sk-049dcb5f22624096b7549c2d2756e45d"
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 智能体回答函数
def fashion_agent_answer(query):
    # 构建消息
    messages = [
        {"role": "system", "content": "你是一名专业的服装电商运营智能体，回答要贴合电商场景，简洁实用。"},
        {"role": "user", "content": query}
    ]
    
    # 调用通义千问大模型生成回复（使用OpenAI兼容API）
    client = openai.OpenAI(
        api_key=DASHSCOPE_API_KEY,
        base_url=DASHSCOPE_BASE_URL
    )
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=messages,
            max_tokens=512,
            temperature=0.7
        )
        # 处理回答格式
        answer = response.choices[0].message.content
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
        return f"❌ 回答失败：{str(e)}"

# API端点
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    if not query:
        return jsonify({"error": "请输入问题"}), 400
    
    # 获取AI回答
    answer = fashion_agent_answer(query)
    return jsonify({"answer": answer})

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)