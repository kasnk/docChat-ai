from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChunkData(BaseModel):
    documentId: str
    text: str
    embedding: List[float]
    createdAt: Optional[datetime]