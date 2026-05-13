from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/auth.test")
async def auth_test():
    return {"ok": True, "team_id": "T_MOCK", "user_id": "U_MOCK"}

@app.post("/api/files.info")
async def files_info():
    return {"ok": True, "file": {"id": "F_MOCK", "name": "mock.csv"}}

@app.post("/api/files.share")
async def files_share():
    return {"ok": True}

@app.post("/api/canvases.edit")
async def canvases_edit():
    return {"ok": True}

@app.post("/api/chat.postMessage")
async def chat_postmessage():
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
