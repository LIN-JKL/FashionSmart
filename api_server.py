from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    logger.info("Root endpoint called")
    return {"message": "Hello World"}

@app.get("/api/health")
async def health():
    logger.info("Health endpoint called")
    return {"status": "ok"}

@app.post("/api/chat")
async def chat(request: Request):
    logger.info("Chat endpoint called")
    try:
        # 直接从请求体读取数据
        body = await request.body()
        logger.info(f"Raw body: {body}")
        
        # 解析JSON
        payload = json.loads(body)
        logger.info(f"Parsed payload: {payload}")
        
        query = payload.get('query', '')
        logger.info(f"Extracted query: {query}")
        
        response = {"answer": f"收到：{query}"}
        logger.info(f"Returning response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        return {"error": "Internal server error"}, 500

# 直接运行uvicorn
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)