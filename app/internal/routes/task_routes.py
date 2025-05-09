from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, status, HTTPException

from app.internal.repository.postgresql.task_repository import TaskRepository
from app.internal.services.task_services import TaskService
from app.pkg.models.app.task_models import Task, TaskStatus
from app.pkg.models.exceptions.task_models import TaskNotFound

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_task_service() -> TaskService:
    return TaskService(TaskRepository())

@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task: Task,
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    return await task_service.create_task(task)

@router.get(
    "/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
)
async def read_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    try:
        return await task_service.read_task(task_id)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except TaskNotFound:
        raise HTTPException(404, detail="Task not found")

@router.get(
    "/",
    response_model=List[Task],
    status_code=status.HTTP_200_OK,
)
async def read_all_tasks(
    due_date: Optional[datetime] = None,
    status: Optional[TaskStatus] = None,
    task_service: TaskService = Depends(get_task_service),
) -> List[Task]:
    return await task_service.read_all_tasks(due_date=due_date, status=status)

@router.put(
    "/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_id: str,
    task: Task,
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    task.id = task_id
    return await task_service.update_task(task)

@router.delete(
    "/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
)
async def delete_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    return await task_service.delete_task(task_id)