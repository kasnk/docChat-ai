from fastapi import APIRouter
from backend.db.mongo_client import chunks_col
from backend.core.embedder import get_embeddings
from datetime import datetime

router = APIRouter()

@router.post("/embed-chunks/{document_id}")
def embed_chunks(document_id: str):
    # Retrieve chunks with text but no embeddings yet
    chunks = list(chunks_col.find({
        "documentId": document_id,
        "embedding": None
    }))

    if not chunks:
        return {"error": "No unembedded chunks found for this document."}

    texts = [chunk.get("text", "") for chunk in chunks if chunk.get("text", "")]
    if not texts:
        return {"error": "Chunks exist but contain no text."}

    embeddings = get_embeddings(texts)

    updated = 0
    for chunk, emb in zip(chunks, embeddings):
        chunks_col.update_one(
            {"_id": chunk["_id"]},
            {"$set": {
                "embedding": emb,
                "createdAt": datetime.utcnow()
            }}
        )
        updated += 1

    return {
        "message": "Embeddings successfully stored.",
        "updatedChunks": updated
    }