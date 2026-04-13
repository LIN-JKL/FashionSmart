from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import sys
import os

# 打印Python版本和环境信息
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Environment variables: {dict(os.environ)}")

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root_get():
    print("Received GET request to /")
    return {"message": "GET request received"}

@app.post("/")
async def root_post(request: Request):
    print("Received POST request to /")
    print(f"Request headers: {dict(request.headers)}")
    body = await request.body()
    print(f"Request body: {body}")
    return {"message": "POST request received"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)