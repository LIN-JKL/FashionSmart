from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求模型
class ChatRequest(BaseModel):
    query: str

@app.get('/')
def home():
    return {"message": "Hello World"}

@app.get('/api/health')
def health():
    return {"status": "ok"}

@app.post('/api/chat')
def chat(request: ChatRequest):
    return {"answer": f"收到：{request.query}"}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host='0.0.0.0', port=port)