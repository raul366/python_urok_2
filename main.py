from fastapi import FastAPI, HTTPException, status
from .schemas import STaskAdd, STask

app = FastAPI()

tasks = []

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task: STaskAdd) -> STask:
    task_dict = task.model_dump()
    task_dict["id"] = 1
    tasks.append(task_dict)
    return task_dict

@app.get("/tasks/{task_id}", response_model=STask)
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {task_id} не найдена"
    )

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task_id == task["id"]:
            tasks.pop(index)
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {task_id} не найдена"
    )