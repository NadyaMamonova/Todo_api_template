from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException

from app.internal.repository.postgresql.task_repository import TaskRepository
from app.pkg.models.app.task_models import Task, TaskStatus
from app.pkg.models.exceptions.task_models import TaskNotFound

class TaskService:
    def __init__(self, repository: TaskRepository):
        self._repository = repository

    async def create_task(self, task: Task) -> Task:
        try:
            return await self._repository.create(task)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )

    async def read_task(self, task_id: str) -> Task:
        try:
            return await self._repository.read(task_id)
        except TaskNotFound as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def read_all_tasks(
        self,
        due_date: Optional[datetime] = None,
        status: Optional[TaskStatus] = None,
    ) -> List[Task]:
        return await self._repository.read_all(due_date=due_date, status=status)

    async def update_task(self, task: Task) -> Task:
        return await self._repository.update(task)

    async def delete_task(self, task_id: str) -> Task:
        return await self._repository.delete(task_id)

def get_task_service() -> TaskService:
    return TaskService(TaskRepository())