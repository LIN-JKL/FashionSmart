from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

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
    return {"status": "ok"}

@app.post("/api/chat")
async def chat(payload: dict = Body(...)):
    logger.info(f"Chat request received: {payload}")
    try:
        query = payload.get('query', '')
        response = {"answer": f"收到：{query}"}
        return response
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        return {"error": "Internal server error"}, 500

# 如果使用 uvicorn 直接运行此文件，不需要下面的 if 块
# 但保留以便本地测试
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)