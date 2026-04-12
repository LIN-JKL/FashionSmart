from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post('/api/chat')
def chat(query: Query):
    return {"answer": "Hello from FastAPI!"}

@app.get('/api/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host='0.0.0.0', port=port)