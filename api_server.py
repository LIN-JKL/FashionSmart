from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
import re

# Try to import vectorstore dependencies
try:
    from langchain.vectorstores import Chroma
    from langchain_community.embeddings import DashScopeEmbeddings
    VECTORSTORE_AVAILABLE = True
except ImportError:
    print("Warning: Vectorstore dependencies not available. Using fallback mode.")
    VECTORSTORE_AVAILABLE = False

# 配置项
CHROMA_DB_PATH = r"d:\创新创业作业\服装向量库"
DASHSCOPE_API_KEY = "sk-049dcb5f22624096b7549c2d2756e45d"
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化向量库
db = None
if VECTORSTORE_AVAILABLE:
    os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY
    try:
        # 使用通义千问的embedding模型
        embeddings = DashScopeEmbeddings(model="text-embedding-v1", dashscope_api_key=DASHSCOPE_API_KEY)
        # 加载现有的向量库
        db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        print("Vector database loaded successfully")
    except Exception as e:
        print(f"Warning: Failed to load vector database: {e}")
        print("Continuing without vector database...")
        db = None
else:
    print("Vectorstore dependencies not available. Using fallback mode.")

# 智能体回答函数
def fashion_agent_answer(query, db):
    # 从RAG知识库检索最相关的内容
    if db is not None:
        try:
            docs = db.similarity_search(query, k=2)
            context = "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"警告：向量库检索失败，将使用默认回答: {str(e)}")
            context = "服装行业相关知识"
    else:
        context = "服装行业相关知识"
    
    # 构建消息
    messages = [
        {"role": "system", "content": "你是一名专业的服装电商运营智能体，需根据以下服装行业专属知识回答问题，回答要贴合电商场景，简洁实用："},
        {"role": "user", "content": f"【服装专属知识】：{context}\n【用户问题】：{query}"}
    ]
    
    # 调用通义千问大模型生成回复（使用OpenAI兼容API）
    openai.api_key = DASHSCOPE_API_KEY
    openai.base_url = DASHSCOPE_BASE_URL
    try:
        response = openai.ChatCompletion.create(
            model="qwen-turbo",
            messages=messages,
            max_tokens=512,
            temperature=0.7
        )
        return response.choices[0].message.content
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
    answer = fashion_agent_answer(query, db)
    return jsonify({"answer": answer})

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)