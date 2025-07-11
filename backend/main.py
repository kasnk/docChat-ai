from fastapi import FastAPI
from backend.api import upload, embed, query
from backend.core.scheduler import setup_ttl_index


app = FastAPI()
app.include_router(upload.router)
app.include_router(embed.router)
app.include_router(query.router)




@app.on_event("startup")
def startup_event():
    setup_ttl_index()

@app.get("/")
def read_root():
    return {"message": "DocuChat API is running!"}