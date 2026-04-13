from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
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

@app.get('/')
def home():
    return {"message": "Hello World"}

@app.get('/api/health')
def health():
    return {"status": "ok"}

@app.post('/api/chat')
def chat(query: str = Body(..., embed=True)):
    return {"answer": f"收到：{query}"}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host='0.0.0.0', port=port)