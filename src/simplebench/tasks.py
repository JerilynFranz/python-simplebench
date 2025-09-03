# -*- coding: utf-8 -*-
"""Container for managing progress tasks."""
from typing import Optional
from rich.progress import Progress, TaskID

from .exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag


class RichTask:
    """Represents and controls a Rich Progress task."""
    def __init__(self, name: str, description: str, progress: Optional[Progress] = None) -> None:
        """Construct a new RichTask.

        Args:
            name (str): The name of the task.
            description (str): The description of the task.
            progress (Optional[Progress]): The Progress instance to use. If omitted,
                a new Progress instance will be created.
        """
        if not isinstance(name, str):
            raise SimpleBenchTypeError(
                f'Expected name arg are to be a str, got {type(name)}',
                ErrorTag.RICH_TASK_INIT_INVALID_NAME_ARG)
        if not name:
            raise SimpleBenchValueError(
                'name arg cannot be an empty string',
                ErrorTag.RICH_TASK_INIT_EMPTY_STRING_NAME)
        if not isinstance(description, str):
            raise SimpleBenchTypeError(
                f'Expected description arg to be a str, got {type(description)}',
                ErrorTag.RICH_TASK_INIT_INVALID_DESCRIPTION_ARG)
        if not description:
            raise SimpleBenchValueError(
                'description arg cannot be an empty string',
                ErrorTag.RICH_TASK_INIT_EMPTY_STRING_DESCRIPTION)
        if progress and not isinstance(progress, Progress):
            raise SimpleBenchTypeError(
                f'Expected progress arg to be a Progress instance, got {type(progress)}',
                ErrorTag.RICH_TASK_INIT_INVALID_PROGRESS_ARG)
        self._name: str = name
        self._description: str = description
        self._progress: Progress = progress if progress and isinstance(progress, Progress) else Progress()
        self._task_id: TaskID = self._progress.add_task(description=self._description)

    def start(self) -> None:
        if self._task_id:
            self._progress.start_task(self._task_id)

    def stop(self) -> None:
        if self._task_id:
            self._progress.stop_task(self._task_id)

    def update(self, completed: int) -> None:
        if self._task_id:
            self._progress.update(task_id=self._task_id, completed=completed)


class RichProgressTasks:
    """Task Rich Progress management for benchmarking."""
    def __init__(self) -> None:
        """Initialize a new RichProgressTasks instance."""
        self._progress = Progress()
        self._task_ids = {}
        self._tasks = {}

    def new_task(self, name: str, description: Optional[str] = None, total: int = 0) -> RichTask:
        """Create a new RichTask.

        Args:
            name (str): The name of the task.
            description (str): The description of the task.
            total (int): The total number of steps for the task.
            completed (int): Number of steps completed (default = 0)
        """
        task: RichTask = RichTask(progress=self._progress, description=name, total=total)
        self._task_ids[name] = task
        return task

    def get_task(self, name: str, description: Optional[str] = None) -> RichTask:
        if task_name in self._tasks:
            return self._tasks[task_name]
        task_id = self._progress.add_task(description=task_name)
        self._task_ids[task_id] = task_name
        self._tasks[task_name] = RichTask(progress=self._progress, description=task_name)
        return self._tasks[task_name]