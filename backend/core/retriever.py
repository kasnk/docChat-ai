from backend.db.mongo_client import chunks_col
from langchain_cohere import CohereEmbeddings  # 👈 Updated import
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

def load_documents(document_id: str) -> list[Document]:
    embedded_chunks = list(chunks_col.find({
        "documentId": document_id,
        "embedding": {"$ne": None}
    }))

    if not embedded_chunks:
        raise ValueError("No embedded chunks found for this document.")

    return [
        Document(page_content=chunk["text"], metadata={"source": str(chunk["_id"])})
        for chunk in embedded_chunks
    ]

def build_vector_store(documents: list[Document]) -> FAISS:
    embedding_model = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model="embed-english-light-v3.0"  # Or any valid Cohere embed model
    )    
    return FAISS.from_documents(documents, embedding=embedding_model)

def generate_response(document_id: str, query: str) -> str:
    try:
        documents = load_documents(document_id)
        vector_store = build_vector_store(documents)

        chat_model = init_chat_model(model="command-a-03-2025", config={"api_key": COHERE_API_KEY},model_provider="cohere")
        qa_chain = RetrievalQA.from_chain_type(
            llm=chat_model,
            retriever=vector_store.as_retriever(),
            return_source_documents=False
        )

        result = qa_chain.run({"query":query})
        return {"response":result}

    except ValueError as ve:
        print(f"❗ Document loading failed: {ve}")
        return f"❗ {str(ve)}"

    except Exception as e:
        print(f"🚨 Retrieval error: {e}")
        return f"🚨 Internal error: {str(e)}"