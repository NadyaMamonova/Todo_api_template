from typing import List, Optional
from uuid import UUID
import logging

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import collect_response
from app.internal.repository.repository import Repository
from app.pkg.models.app.task_models import Task, TaskFields, TaskStatus
from app.pkg.models.exceptions.task_models import TaskNotFound, TaskAlreadyExists

logger = logging.getLogger(__name__)


class TaskRepository(Repository):

    @collect_response
    async def create(self, task: Task) -> Task:
        """Создание задачи с валидацией данных"""
        if not isinstance(task.id, str):
            raise ValueError("Task ID must be a string")

        q = """
        INSERT INTO tasks(id, title, description, created_at, due_date, status)
        VALUES (%(id)s, %(title)s, %(description)s, %(created_at)s, %(due_date)s, %(status)s)
        RETURNING id, title, description, created_at, due_date, status;
        """
        async with get_connection() as cur:
            try:
                await cur.execute(q, task.dict())
                result = await cur.fetchone()
                return Task(**result)
            except Exception as e:
                if "duplicate key value" in str(e):
                    raise TaskAlreadyExists
                logger.error(f"Error creating task: {e}")
                raise

    @collect_response
    async def read(self, task_id: str) -> Task:
        """Получение задачи по ID с проверкой существования"""
        try:
            UUID(task_id)  # Валидация UUID
        except ValueError as e:
            logger.warning(f"Invalid task ID format: {task_id}")
            raise TaskNotFound from e

        q = """
        SELECT id, title, description, created_at, due_date, status 
        FROM tasks 
        WHERE id = %(id)s;
        """
        async with get_connection() as cur:
            try:
                await cur.execute(q, {"id": task_id})
                result = await cur.fetchone()
                if not result:
                    raise TaskNotFound
                return Task(**result)
            except Exception as e:
                logger.error(f"Error reading task {task_id}: {e}")
                raise

    @collect_response
    async def read_all(self) -> List[Task]:
        """Получение всех задач с обработкой пустого результата"""
        q = """
        SELECT id, title, description, created_at, due_date, status 
        FROM tasks
        ORDER BY created_at DESC;
        """
        async with get_connection() as cur:
            try:
                await cur.execute(q)
                results = await cur.fetchall()
                return [Task(**dict(row)) for row in results]
            except Exception as e:
                logger.error(f"Error reading tasks: {e}")
                raise

    @collect_response
    async def update(self, task: Task) -> Task:
        """Обновление задачи с полной проверкой данных"""
        q = """
        UPDATE tasks SET
            title = %(title)s,
            description = %(description)s,
            due_date = %(due_date)s,
            status = %(status)s
        WHERE id = %(id)s
        RETURNING id, title, description, created_at, due_date, status;
        """
        async with get_connection() as cur:
            try:
                await cur.execute(q, task.dict())
                result = await cur.fetchone()
                if not result:
                    raise TaskNotFound
                return Task(**result)
            except Exception as e:
                logger.error(f"Error updating task {task.id}: {e}")
                raise

    @collect_response
    async def delete(self, task_id: str) -> Task:
        """Удаление задачи с проверкой существования"""
        try:
            UUID(task_id)  # Валидация UUID
        except ValueError as e:
            logger.warning(f"Invalid task ID format: {task_id}")
            raise TaskNotFound from e

        q = """
        DELETE FROM tasks 
        WHERE id = %(id)s 
        RETURNING id, title, description, created_at, due_date, status;
        """
        async with get_connection() as cur:
            try:
                await cur.execute(q, {"id": task_id})
                result = await cur.fetchone()
                if not result:
                    raise TaskNotFound
                return Task(**result)
            except Exception as e:
                logger.error(f"Error deleting task {task_id}: {e}")
                raise