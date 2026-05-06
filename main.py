from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Task Manager API",
    description="Учебное приложение для курса по FastAPI",
    version="1.0.0"
)

# 1. Модель данных (схема)
# Она гарантирует, что пользователь всегда имеет имя и возраст
class User(BaseModel):
    id: int
    name: str
    age: int

# 2. Наша "База данных"
users_db = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
    {"id":3, "name": "Charlie", "age": 21},
]

fake_tasks_db = [
    {"task_name": "Task 1"},
    {"task_name": "Task 2"},
    {"task_name": "Task 3"},
    {"task_name": "Task 4"},
    {"task_name": "Task 5"},
    {"task_name": "Task 6"},
    {"task_name": "Task 7"},
    {"task_name": "Task 8"},
    {"task_name": "Task 9"},
    {"task_name": "Task 10"},
]

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

from pydantic import BaseModel

class STask(BaseModel):
    name: str
    description: str
    is_done: bool
    priority: int

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}

@app.post("/create")
async def create():
    return {"status": "created"}

@app.get("/users")
def get_all_users(is_admin:bool = False):
    """Возвращает список всех пользователей"""
    return {"admin_mode": is_admin}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Возвращает конкретного пользователя по ID"""
    for user in users_db:
        if user["id"] == user_id:
            return {"name": user["name"]}
    # Если не нашли — выдаем ошибку 404
    return {"error": "User not found"}

@app.post("/users")
def create_user(user: User):
    """Добавляет нового пользователя"""
    # Превращаем модель Pydantic в словарь и добавляем в список
    users_db.append(user.dict())
    return {"message": "User created", "user": user}

@app.put("/users/{user_id}")
def update_user_complete(user_id: int, updated_user: User):
    """Полностью заменяет пользователя с указанным ID"""
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            # Полная замена элемента списка
            users_db[index] = updated_user.dict()
            return {"message": "User updated completely", "user": updated_user}
    
    raise HTTPException(status_code=404, detail="User not found")

@app.patch("/users/{user_id}")
def update_user_partial(user_id: int, user_update: UserUpdate):
    """Обновляет только переданные поля"""
    for user in users_db:
        if user["id"] == user_id:
            # Если прислали имя — обновляем имя
            if user_update.name is not None:
                user["name"] = user_update.name
            # Если прислали возраст — обновляем возраст
            if user_update.age is not None:
                user["age"] = user_update.age
            return {"message": "User updated partially", "user": user}
            
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Удаляет пользователя по ID"""
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            del users_db[index] # Удаляем из списка
            return {"message": f"User {user_id} deleted"}
            
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/tasks/{tasks_id}")
def get_tasks(tasks_id: int):
    for task in fake_tasks_db:
        if task["task_id"] == tasks_id:
            return task
    return {}

@app.get("/tasks")
async def get_tasks(limit: int = 10, offset: int = 0, keyword: str | None = None):
    if keyword is None:
        return fake_tasks_db[offset:offset + limit]
    else:
        sorted_tasks = []
        for task in fake_tasks_db:
            if keyword.lower() in task["task_name"].lower():
                sorted_tasks.append(task)
        return sorted_tasks[offset:offset + limit]

@app.get("/hello/{name}")
def get_hello(name):
    return {"message": "Hello, " + name + "!"}

@app.get("/product/{product_id}")
def get_product(product_id:int):
    return {"product_id": product_id}

@app.get("/flights/{from_code}/{to_code}")
def get_flights(from_code, to_code):
    return {"from": from_code, "to": to_code}

@app.get("/files/{file_path:path}")
def get_files(file_path):
    return {"file": file_path}

@app.get("/items")
async def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/login")
async def get_login(username: str, password: str):
    return {"user": username, "password": password}

@app.get("/search")
async def get_search(query: str | None = None):
    if query:
        return {"msg": f"Searching for {query}"}
    else:
        return {"msg": "Showing all results"}

@app.get("/multiply")
async def get_multiply(value: int, multiplier: int = 2):
    return {"result": value * multiplier}

@app.get("/sum")
async def get_sum(a: int, b: int):
    return {"result": a + b}

# Добавляем этот блок в конец файла
if __name__ == "__main__":
    # Обратите внимание: имя файла передается как строка
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)