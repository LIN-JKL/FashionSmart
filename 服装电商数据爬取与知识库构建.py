import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import openai
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.dashscope import DashScopeEmbeddings
import dashscope

# -------------------------- 配置项 --------------------------
# 保存路径：替换成你的电脑路径
SAVE_PATH = r"d:\创新创业作业\服装数据"
# 向量库保存路径
CHROMA_DB_PATH = r"d:\创新创业作业\服装向量库"
# 通义千问API-Key
DASHSCOPE_API_KEY = "sk-049dcb5f22624096b7549c2d2756e45d"
# 通义千问API Base URL
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# 爬虫延迟
DELAY = 0.5

# 确保文件夹存在
os.makedirs(SAVE_PATH, exist_ok=True)
os.makedirs(CHROMA_DB_PATH, exist_ok=True)

# -------------------------- 1. 爬取淘宝服装热搜词 --------------------------
def crawl_taobao_fashion_hotwords():
    try:
        url = "https://s.taobao.com/search?q=服装&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        # 提取热搜词
        hotwords = []
        for item in soup.select(".search-hot-keyword a"):
            word = item.get_text(strip=True)
            if word and len(word) > 1:
                hotwords.append(word)
        # 去重并保存
        hotwords = list(set(hotwords))[:50]  # 取前50个核心热搜词
        df_hot = pd.DataFrame({"服装热搜词": hotwords})
        df_hot.to_csv(SAVE_PATH + "淘宝服装热搜词.csv", index=False, encoding="utf-8-sig")
        print("✅ 淘宝服装热搜词爬取完成，保存至：淘宝服装热搜词.csv")
        return hotwords
    except Exception as e:
        print(f"❌ 淘宝热搜词爬取失败：{e}")
        # 内置热搜词作为兜底
        default_hotwords = ["梨形身材牛仔裤", "多巴胺色系连衣裙", "软糯亲肤卫衣", "法式雪纺连衣裙", "高腰显瘦", "微喇设计", "冰丝面料", "纯棉T恤", "加绒卫衣", "童装连帽卫衣"]
        df_hot = pd.DataFrame({"服装热搜词": default_hotwords})
        df_hot.to_csv(SAVE_PATH + "淘宝服装热搜词.csv", index=False, encoding="utf-8-sig")
        return default_hotwords

# -------------------------- 2. 爬取小红书服装爆款文案 --------------------------
def crawl_xhs_fashion_copy():
    try:
        # 小红书服装推荐页（公开数据，无反爬）
        url = "https://www.xiaohongshu.com/search_result?keyword=服装爆款推荐&source=web"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        # 提取文案
        copy_writing = []
        for item in soup.select(".note-content"):
            copy = item.get_text(strip=True).replace("\n", "").replace(" ", "")
            if copy and len(copy) > 20:  # 过滤短文案
                copy_writing.append(copy)
        # 去重并保存
        copy_writing = list(set(copy_writing))[:30]  # 取前30条爆款文案
        df_copy = pd.DataFrame({"服装爆款文案": copy_writing})
        df_copy.to_csv(SAVE_PATH + "小红书服装文案.csv", index=False, encoding="utf-8-sig")
        print("✅ 小红书服装文案爬取完成，保存至：小红书服装文案.csv")
        return copy_writing
    except Exception as e:
        print(f"❌ 小红书文案爬取失败：{e}")
        # 内置文案作为兜底
        default_copy = ["梨形身材姐妹锁死这条牛仔裤！微喇版型遮胯显腿长，高腰设计提臀，软乎乎的牛仔面料，搭T恤/衬衫都好看～", "法式雪纺连衣裙太温柔了！收腰设计显瘦，面料轻薄透气，夏天穿正合适，约会通勤都能穿。", "纯棉T恤yyds！柔软亲肤，透气吸汗，基础款百搭，随便搭牛仔裤、半身裙都好看。", "加绒卫衣太保暖了！宽松版型，穿上超舒服，秋冬必备，搭卫裤、牛仔裤都很时尚。", "童装连帽卫衣可爱到爆炸！纯棉面料，柔软亲肤，孩子穿上超开心，春秋季节正好穿。"]
        df_copy = pd.DataFrame({"服装爆款文案": default_copy})
        df_copy.to_csv(SAVE_PATH + "小红书服装文案.csv", index=False, encoding="utf-8-sig")
        return default_copy

# -------------------------- 3. 爬取服装通用客服问答 --------------------------
def crawl_fashion_qa():
    # 直接爬取公开的服装客服问答库（也可手动补充，课程作业够用）
    try:
        url = "https://www.zhidao.baidu.com/question/123456789.html"  # 服装问答通用页
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        # 提取问答（若爬取失败，自动使用内置通用问答，保证数据可用）
        qa_list = []
        # 内置服装通用问答（兜底，避免爬虫失败）
        default_qa = [
            {"问题": "160cm/90斤穿什么码？", "答案": "建议穿S码，标准版型，该尺码适配155-162cm/80-95斤的人群"},
            {"问题": "雪纺面料容易勾丝吗？", "答案": "雪纺面料质地轻薄，轻微勾丝，建议避免接触尖锐物品，清洗时轻柔手洗"},
            {"问题": "纯棉T恤可以机洗吗？", "答案": "可以机洗，建议用冷水轻柔模式，避免暴晒，防止缩水"},
            {"问题": "微喇牛仔裤适合梨形身材吗？", "答案": "非常适合，微喇版型能修饰胯宽和大腿粗，视觉上显腿长，梨形身材闭眼入"},
            {"问题": "卫衣的加绒款会掉毛吗？", "答案": "优质加绒卫衣轻微浮毛，第一次清洗用冷水加盐浸泡10分钟，可有效减少掉毛"},
            {"问题": "发货时间是多久？", "答案": "一般情况下，我们会在48小时内发货，部分热销商品可能会延迟1-2天"},
            {"问题": "支持退换货吗？", "答案": "支持7天无理由退换货，非质量问题运费自理，质量问题我们承担运费"},
            {"问题": "有运费险吗？", "答案": "是的，我们所有商品都支持运费险，退换货产生的运费由保险公司承担"},
            {"问题": "尺码不合适可以换吗？", "答案": "可以的，尺码不合适可以申请换货，来回运费由运费险承担"},
            {"问题": "未付款的订单会保留多久？", "答案": "未付款的订单会保留24小时，超过24小时系统会自动取消"},
            {"问题": "老客户有什么优惠？", "答案": "老客户可以享受会员折扣，消费满1000元升级为银卡会员，享受95折；满3000元升级为金卡会员，享受9折；满5000元升级为钻石会员，享受85折"},
            {"问题": "上新通知怎么获取？", "答案": "您可以关注我们的店铺，设置上新提醒，或者加入我们的会员群，第一时间获取上新信息"}
        ]
        # 若爬虫成功则合并，失败则用内置
        if soup.select(".wgt-answers-content"):
            for item in soup.select(".wgt-answers-content")[:10]:
                qa_list.append({"问题": item.previous_sibling.get_text(strip=True), "答案": item.get_text(strip=True)})
        qa_list = qa_list + default_qa
        # 去重并保存
        df_qa = pd.DataFrame(qa_list).drop_duplicates(subset=["问题"])
        df_qa.to_csv(SAVE_PATH + "服装客服问答.csv", index=False, encoding="utf-8-sig")
        print("✅ 服装客服问答爬取完成，保存至：服装客服问答.csv")
        return qa_list
    except Exception as e:
        print(f"❌ 客服问答爬取失败，使用内置通用问答：{e}")
        default_qa = [
            {"问题": "160cm/90斤穿什么码？", "答案": "建议穿S码，标准版型，该尺码适配155-162cm/80-95斤的人群"},
            {"问题": "雪纺面料容易勾丝吗？", "答案": "雪纺面料质地轻薄，轻微勾丝，建议避免接触尖锐物品，清洗时轻柔手洗"},
            {"问题": "纯棉T恤可以机洗吗？", "答案": "可以机洗，建议用冷水轻柔模式，避免暴晒，防止缩水"},
            {"问题": "微喇牛仔裤适合梨形身材吗？", "答案": "非常适合，微喇版型能修饰胯宽和大腿粗，视觉上显腿长，梨形身材闭眼入"},
            {"问题": "卫衣的加绒款会掉毛吗？", "答案": "优质加绒卫衣轻微浮毛，第一次清洗用冷水加盐浸泡10分钟，可有效减少掉毛"},
            {"问题": "发货时间是多久？", "答案": "一般情况下，我们会在48小时内发货，部分热销商品可能会延迟1-2天"},
            {"问题": "支持退换货吗？", "答案": "支持7天无理由退换货，非质量问题运费自理，质量问题我们承担运费"},
            {"问题": "有运费险吗？", "答案": "是的，我们所有商品都支持运费险，退换货产生的运费由保险公司承担"},
            {"问题": "尺码不合适可以换吗？", "答案": "可以的，尺码不合适可以申请换货，来回运费由运费险承担"},
            {"问题": "未付款的订单会保留多久？", "答案": "未付款的订单会保留24小时，超过24小时系统会自动取消"},
            {"问题": "老客户有什么优惠？", "答案": "老客户可以享受会员折扣，消费满1000元升级为银卡会员，享受95折；满3000元升级为金卡会员，享受9折；满5000元升级为钻石会员，享受85折"},
            {"问题": "上新通知怎么获取？", "答案": "您可以关注我们的店铺，设置上新提醒，或者加入我们的会员群，第一时间获取上新信息"}
        ]
        df_qa = pd.DataFrame(default_qa)
        df_qa.to_csv(SAVE_PATH + "服装客服问答.csv", index=False, encoding="utf-8-sig")
        return default_qa

# -------------------------- 4. 整合清洗数据 --------------------------
def integrate_data():
    # 读取3个CSV文件
    df_hot = pd.read_csv(SAVE_PATH + "淘宝服装热搜词.csv", encoding="utf-8-sig")
    df_copy = pd.read_csv(SAVE_PATH + "小红书服装文案.csv", encoding="utf-8-sig")
    df_qa = pd.read_csv(SAVE_PATH + "服装客服问答.csv", encoding="utf-8-sig")
    
    # 格式化整合为纯文本
    SAVE_TXT_PATH = SAVE_PATH + "服装电商知识库.txt"
    with open(SAVE_TXT_PATH, "w", encoding="utf-8") as f:
        # 1. 服装热搜词
        f.write("=== 淘宝服装高流量热搜词 ===\n")
        for word in df_hot["服装热搜词"]:
            f.write(f"{word}\n")
        f.write("\n")
        # 2. 服装爆款文案
        f.write("=== 小红书服装爆款文案 ===\n")
        for copy in df_copy["服装爆款文案"]:
            f.write(f"{copy}\n")
        f.write("\n")
        # 3. 服装客服问答
        f.write("=== 服装客服通用问答 ===\n")
        for idx, row in df_qa.iterrows():
            f.write(f"问题：{row['问题']}\n答案：{row['答案']}\n\n")
    
    print(f"✅ 服装数据整合完成，已生成纯文本知识库：{SAVE_TXT_PATH}")
    return SAVE_TXT_PATH

# -------------------------- 5. 构建RAG知识库 --------------------------
def build_rag_knowledge_base(txt_path):
    # 加载纯文本知识库
    loader = TextLoader(txt_path, encoding="utf-8")
    documents = loader.load()
    print(f"✅ 成功加载服装知识库，总字符数：{len(documents[0].page_content)}")
    
    # 拆分文本
    text_splitter = CharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        separator="\n",
        strip_whitespace=True
    )
    texts = text_splitter.split_documents(documents)
    print(f"✅ 文本拆分完成，生成{len(texts)}个检索片段")
    
    # 初始化通义千问Embedding
    os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY
    embeddings = DashScopeEmbeddings(model="text-embedding-v1")
    
    # Chroma存储向量，构建RAG知识库
    db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    # 持久化数据库
    db.persist()
    
    # 验证：检索一次测试
    test_query = "160/90斤穿什么码？"
    docs = db.similarity_search(test_query, k=1)
    print(f"\n🚀 RAG知识库构建完成！本地向量库保存至：{CHROMA_DB_PATH}")
    print(f"🔍 测试检索「{test_query}」，匹配结果：{docs[0].page_content}")
    
    return db

# -------------------------- 6. 定义智能体回答函数 --------------------------
def fashion_agent_answer(query, db):
    # 从RAG知识库检索最相关的内容
    docs = db.similarity_search(query, k=2)
    context = "\n".join([doc.page_content for doc in docs])
    
    # 构建提示词
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

# -------------------------- 主函数 --------------------------
if __name__ == "__main__":
    print("🚀 开始爬取服装电商数据...")
    # 1. 爬取数据
    crawl_taobao_fashion_hotwords()
    time.sleep(DELAY)
    crawl_xhs_fashion_copy()
    time.sleep(DELAY)
    crawl_fashion_qa()
    
    # 2. 整合数据
    txt_path = integrate_data()
    
    # 3. 构建RAG知识库
    db = build_rag_knowledge_base(txt_path)
    
    # 4. 测试智能体功能
    print("\n🧪 测试服装电商智能体功能...")
    # 测试1：客服问答
    query1 = "160cm/95斤穿什么码？"
    # 测试2：标题生成
    query2 = "生成法式雪纺连衣裙的淘宝标题，嵌入热搜词"
    # 测试3：文案生成
    query3 = "生成梨形身材牛仔裤的小红书种草文案"
    
    print(f"📌 问题1：{query1}")
    print(f"💡 回答1：{fashion_agent_answer(query1, db)}\n")
    
    print(f"📌 问题2：{query2}")
    print(f"💡 回答2：{fashion_agent_answer(query2, db)}\n")
    
    print(f"📌 问题3：{query3}")
    print(f"💡 回答3：{fashion_agent_answer(query3, db)}")
    
    print("\n🎉 所有功能测试完成！")