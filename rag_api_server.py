from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import pandas as pd

# 配置项
DASHSCOPE_API_KEY = "sk-049dcb5f22624096b7549c2d2756e45d"
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置字符编码
app.config['JSON_AS_ASCII'] = False

# 加载知识库数据
def load_knowledge_base():
    knowledge_base = []
    
    # 检查是否存在服装数据文件夹
    data_path = r"d:\创新创业作业\服装数据"
    if os.path.exists(data_path):
        # 加载淘宝服装热搜词
        hotwords_file = os.path.join(data_path, "淘宝服装热搜词.csv")
        if os.path.exists(hotwords_file):
            df = pd.read_csv(hotwords_file, encoding="utf-8-sig")
            for _, row in df.iterrows():
                knowledge_base.append(f"服装热搜词：{row['服装热搜词']}")
        
        # 加载小红书服装文案
        copy_file = os.path.join(data_path, "小红书服装文案.csv")
        if os.path.exists(copy_file):
            df = pd.read_csv(copy_file, encoding="utf-8-sig")
            for _, row in df.iterrows():
                knowledge_base.append(f"服装文案：{row['服装爆款文案']}")
        
        # 加载服装问答
        qa_file = os.path.join(data_path, "服装通用问答.csv")
        if os.path.exists(qa_file):
            df = pd.read_csv(qa_file, encoding="utf-8-sig")
            for _, row in df.iterrows():
                knowledge_base.append(f"问题：{row['问题']}，答案：{row['答案']}")
    
    # 如果知识库为空，添加一些默认知识
    if not knowledge_base:
        default_knowledge = [
            "服装热搜词：梨形身材牛仔裤",
            "服装热搜词：多巴胺色系连衣裙",
            "服装热搜词：软糯亲肤卫衣",
            "服装热搜词：法式雪纺连衣裙",
            "服装热搜词：高腰显瘦",
            "服装文案：梨形身材姐妹锁死这条牛仔裤！微喇版型遮胯显腿长，高腰设计提臀，软乎乎的牛仔面料，搭T恤/衬衫都好看～",
            "服装文案：法式雪纺连衣裙太温柔了！收腰设计显瘦，面料轻薄透气，夏天穿正合适，约会通勤都能穿。",
            "服装文案：纯棉T恤yyds！柔软亲肤，透气吸汗，基础款百搭，随便搭牛仔裤、半身裙都好看。",
            "问题：160cm/90斤穿什么码？，答案：建议穿S码，标准版型，该尺码适配155-162cm/80-95斤的人群",
            "问题：雪纺面料容易勾丝吗？，答案：雪纺面料质地轻薄，轻微勾丝，建议避免接触尖锐物品，清洗时轻柔手洗"
        ]
        knowledge_base.extend(default_knowledge)
    
    return knowledge_base

# 过滤相关知识库
def get_relevant_knowledge(query, knowledge_base):
    # 确保查询字符串编码正确
    if isinstance(query, bytes):
        query = query.decode('utf-8')
    
    # 定义商品类型关键词映射
    product_keywords = {
        "牛仔裤": ["牛仔裤", "牛仔", "裤", "高腰", "微喇", "版型"],
        "连衣裙": ["连衣裙", "裙子"],
        "雪纺连衣裙": ["雪纺", "连衣裙", "面料"],
        "法式连衣裙": ["法式", "连衣裙", "风格"],
        "T恤": ["T恤", "t恤", "短袖", "体恤"]
    }
    
    # 识别用户查询中的商品类型
    detected_products = []
    
    # 优先识别更具体的商品类型
    if "法式雪纺连衣裙" in query:
        detected_products.append("法式雪纺连衣裙")
        detected_products.append("法式连衣裙")
        detected_products.append("雪纺连衣裙")
    elif "雪纺连衣裙" in query:
        detected_products.append("雪纺连衣裙")
    elif "法式连衣裙" in query:
        detected_products.append("法式连衣裙")
    elif "牛仔裤" in query:
        detected_products.append("牛仔裤")
    elif "连衣裙" in query:
        detected_products.append("连衣裙")
    elif "T恤" in query or "t恤" in query:
        detected_products.append("T恤")
    
    # 筛选与查询相关的知识
    relevant_knowledge = []
    seen_items = set()  # 用于去重
    
    for item in knowledge_base:
        # 如果检测到了商品类型，只保留相关的知识
        if detected_products:
            # 检查该知识是否与任何检测到的商品类型相关
            is_relevant = False
            for product in detected_products:
                if any(keyword in item for keyword in product_keywords.get(product, [])):
                    is_relevant = True
                    break
            # 确保知识与查询中的具体商品相关
            if is_relevant and item not in seen_items:
                # 对于牛仔裤查询，只保留牛仔裤相关知识
                if "牛仔裤" in detected_products and "牛仔裤" not in item:
                    continue
                # 对于连衣裙查询，只保留连衣裙相关知识
                if ("连衣裙" in detected_products or "雪纺连衣裙" in detected_products or "法式连衣裙" in detected_products) and "连衣裙" not in item:
                    continue
                relevant_knowledge.append(item)
                seen_items.add(item)
        else:
            # 如果没有检测到商品类型，返回所有知识
            if item not in seen_items:
                relevant_knowledge.append(item)
                seen_items.add(item)
    
    # 如果没有找到相关知识，返回全部知识
    if not relevant_knowledge:
        relevant_knowledge = knowledge_base
    
    return relevant_knowledge

# 智能体回答函数
def fashion_agent_answer(query):
    # 确保查询字符串编码正确
    if isinstance(query, bytes):
        query = query.decode('utf-8')
    
    # 加载知识库
    knowledge_base = load_knowledge_base()
    
    # 过滤相关知识库
    relevant_knowledge = get_relevant_knowledge(query, knowledge_base)
    
    # 构建上下文
    context = "\n".join(relevant_knowledge)  # 使用相关知识作为上下文
    
    # 提取商品类型
    product_type = ""
    if "牛仔裤" in query:
        product_type = "牛仔裤"
    elif "法式雪纺连衣裙" in query:
        product_type = "法式雪纺连衣裙"
    elif "雪纺连衣裙" in query:
        product_type = "雪纺连衣裙"
    elif "法式连衣裙" in query:
        product_type = "法式连衣裙"
    elif "连衣裙" in query:
        product_type = "连衣裙"
    elif "T恤" in query or "t恤" in query:
        product_type = "T恤"
    else:
        product_type = "服装"
    
    # 构建消息，将知识库内容直接融入到用户查询中
    messages = [
        {
            "role": "system",
            "content": "你是一名专业的服装电商运营智能体，为服装电商提供全方位的服务，包括文案撰写、标题优化、产品咨询、促销信息查询、平台信息查询等。请根据知识库中的相关内容，为用户生成符合电商场景的详细回答。\n\n要求：\n1. 针对不同类型的请求给出不同的专业回答\n2. 具体问题具体分析，根据用户的问题类型生成针对性内容\n3. 提供详细、具体的回答，充分利用知识库中的信息\n4. 参考知识库中的内容，但不要简单复制，要进行扩展和优化\n5. 不要有开场白或问候语，直接给出专业内容\n6. 确保回答符合电商平台的风格和要求\n7. 严格按照用户的问题内容回答，绝对不要偏离主题\n8. 数字范围必须使用波浪线连接，如25~35岁，而不是2535或25-35\n9. 对于促销信息、平台信息等查询，要基于知识库内容提供详细的回答\n10. 如果知识库中没有足够的信息，要基于电商领域的专业知识给出合理的建议"
        },
        {
            "role": "user",
            "content": f"知识库内容：\n{context}\n\n用户请求：{query}\n\n请根据用户的具体问题生成详细的回答。\n1. 如果是文案撰写或标题优化请求，请为{product_type}提供至少3个不同风格的方案，每个方案应包含：\n   - 标题\n   - 目标人群\n   - 商品特点\n   - 使用场景\n   - 促销语\n2. 如果是产品咨询类问题，请直接回答用户的问题，提供详细、专业的解答\n3. 如果是促销信息、平台信息等查询，请基于知识库内容提供详细的回答\n\n请严格针对用户的具体问题回答，不要偏离主题。"
        }
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
    
    query = data.get('query', '') if data else ''
    
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