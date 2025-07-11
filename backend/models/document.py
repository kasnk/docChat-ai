from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentUpload(BaseModel):
    filename: str
    uploadDate: Optional[datetime]
    metadata: Optional[dict] = None