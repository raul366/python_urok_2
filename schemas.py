from pydantic import BaseModel, Field

class STaskAdd(BaseModel):
    # Обязательное поле с валидацией
    name: str = Field(..., min_length=2, max_length=100, description="Название задачи") 
    # Необязательное поле (значение по умолчанию None)
    description: str | None = Field(None, max_length=300)
    priority: int = Field(1, ge= 1, le = 5)

class SUser(BaseModel):
    name: str
    age: int
    is_active: bool = True

class SProduct(BaseModel):
    title: str
    price: int
    description: str | None = None

class SFeedback(BaseModel):
    message: str
    rating: int = Field(1, ge= 1, le = 5)

class SRegistration(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)
    bio: str = Field("", max_length=100)