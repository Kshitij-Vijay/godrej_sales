from pydantic import BaseModel
from typing import List

class TextFileMetadata(BaseModel):
    path: str
    description: str
    embedding: List[List[float]]  # list of embedding vectors (for multiple chunks)
