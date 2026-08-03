from pydantic import BaseModel


class PDFResponse(BaseModel):
    status: str
    chunks: int
    message: str | None = None