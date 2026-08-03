from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    chunks: int
    upload_time: str