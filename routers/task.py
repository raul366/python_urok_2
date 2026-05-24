from fastapi import APIRouter, HTTPException, status
from schemas.task import STaskAdd, STask

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)

tasks = []

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(task: STaskAdd) -> STask:
    task_dict = task.model_dump()
    task_dict["id"] = 1
    tasks.append(task_dict)
    return task_dict

@router.get("/{task_id}", response_model=STask)
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {task_id} не найдена"
    )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task_id == task["id"]:
            tasks.pop(index)
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {task_id} не найдена"
    )
