from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
import os
import logging
from fastapi.middleware.cors import CORSMiddleware

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# 启用CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.post('/api/chat')
async def chat(query: Query):
    logger.info(f"Chat endpoint called with query: {query.query}")
    return {"answer": "Hello from FastAPI!"}

@app.get('/api/health')
async def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    logger.info(f"Python version: {os.sys.version}")
    logger.info(f"Current directory: {os.getcwd()}")
    uvicorn.run(app, host='0.0.0.0', port=port)