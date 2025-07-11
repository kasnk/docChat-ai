from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QueryLog(BaseModel):
    documentId: str
    queryText: str
    responseText: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[dict] = None  # Optional: can include LLM used, tokens, etc.