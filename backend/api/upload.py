from fastapi import APIRouter, File, UploadFile
from backend.db.mongo_client import documents_col, chunks_col
from backend.core.pdf_parser import extract_chunks
from langchain_cohere import CohereEmbeddings
from datetime import datetime
from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    filename = file.filename
    contents = await file.read()

    chunks = extract_chunks(contents)  # Returns list[str]

    # Initialize embedding model
    embedding_model = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model="embed-english-light-v3.0"  # Change if needed
    )

    # Generate embeddings
    embeddings = embedding_model.embed_documents(chunks)

    # Save document metadata
    doc_data = {
        "filename": filename,
        "uploadDate": datetime.utcnow(),
        "chunkCount": len(chunks),
        "pinned": False,
        "metadata": {}
    }
    doc_id = documents_col.insert_one(doc_data).inserted_id

    # Save embedded chunks to MongoDB
    for i, text in enumerate(chunks):
        chunk_doc = {
            "documentId": str(doc_id),
            "text": text,
            "embedding": embeddings[i],
            "createdAt": datetime.utcnow()
        }
        chunks_col.insert_one(chunk_doc)
    
    return {"documentId": str(doc_id), "chunkCount": len(chunks)}