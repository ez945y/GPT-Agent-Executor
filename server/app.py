from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from utils.public_cache import CachePool
app = FastAPI()

@app.post("/api/talk")
async def communicate(request: Request):
    """接收文字並回傳"""
    data = await request.json()
    if not data or "text" not in data:
        return JSONResponse({"error": "缺少文字"}, status_code=400)

    received_text = data["text"]
    await CachePool.add({"user":received_text})
    return JSONResponse({"received_text": received_text})

def run_fastapi_server():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    run_fastapi_server()