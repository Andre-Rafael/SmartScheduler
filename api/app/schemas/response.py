from pydantic import BaseModel


class ResponseSchema(BaseModel):
    id: str
    text: str
