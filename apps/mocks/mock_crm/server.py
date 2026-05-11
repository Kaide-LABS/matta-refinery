from fastapi import FastAPI

app = FastAPI()

@app.post("/hubspot/webhook")
async def hubspot_webhook():
    return {"status": "ok"}

@app.patch("/hubspot/contacts/{contact_id}")
async def hubspot_contact_patch(contact_id: str):
    return {"status": "ok"}

@app.post("/hubspot/contacts/{contact_id}/notes")
async def hubspot_contact_notes(contact_id: str):
    return {"status": "ok"}

@app.post("/salesforce/webhook")
async def salesforce_webhook():
    return {"status": "ok"}

@app.patch("/salesforce/contacts/{contact_id}")
async def salesforce_contact_patch(contact_id: str):
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8091)
