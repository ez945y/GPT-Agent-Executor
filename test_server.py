#!/usr/bin/env python3
"""
簡單的服務器測試腳本
"""

import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    return {"status": "ok"}

if __name__ == "__main__":
    print("🚀 啟動簡單測試服務器...")
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info") 