from pydantic import BaseModel


class PDFResponse(BaseModel):
    status: str
    chunks: int