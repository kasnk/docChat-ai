from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.retriever import generate_response
from backend.db.mongo_client import queries_col
from datetime import datetime

router = APIRouter()

class AskPayload(BaseModel):
    documentId: str
    queryText: str

@router.post("/ask")
def ask(payload: AskPayload):
    try:
        response = generate_response(payload.documentId, payload.queryText)

        queries_col.insert_one({
            "documentId": payload.documentId,
            "queryText": payload.queryText,
            "responseText": response,
            "timestamp": datetime.utcnow()
        })

        return {"response": response}

    except ValueError as ve:
        return {"error": str(ve)}

    except Exception as e:
        return {"error": f"Internal error: {str(e)}"}