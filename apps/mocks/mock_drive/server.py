from fastapi import FastAPI

app = FastAPI()

@app.post("/drive/files")
async def drive_files():
    return {"file_id": "D_MOCK", "web_view_link": "https://drive.google.com/mock"}

@app.patch("/drive/files/{file_id}")
async def drive_files_patch(file_id: str):
    return {"status": "ok"}

@app.post("/drive/files/{file_id}/permissions")
async def drive_files_permissions(file_id: str):
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8092)
