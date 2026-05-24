from pydantic import BaseModel

class STaskBase(BaseModel):
    name: str
    description: str | None = None

class STaskAdd(STaskBase):
    pass

class STask(STaskBase):
    id: int