from pydantic import BaseModel


class ScheduleData(BaseModel):
    id: str
    text: str
