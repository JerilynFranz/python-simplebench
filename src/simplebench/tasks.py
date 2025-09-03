# -*- coding: utf-8 -*-
"""module for managing progress tasks using Rich Progress."""
from typing import Optional

from rich.progress import Progress, TaskID

from .exceptions import (SimpleBenchKeyError, SimpleBenchTypeError,
                         SimpleBenchValueError, SimpleBenchRuntimeError,
                         ErrorTag)


class RichTask:
    """Represents and controls a Rich Progress task."""
    def __init__(self,
                 name: str,
                 description: str,
                 completed: int = 0,
                 total: int = 100,
                 progress: Optional[Progress] = None) -> None:
        """Construct a new RichTask.

        Args:
            name (str): The name of the task.
            description (str): The description of the task.
            completed (Optional[int]): Completion step (default=0)
            total (Optional[int]): Total number of steps (default=100)
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
        """The name of the task."""
        self._description: str = description
        """The description of the task."""
        self._progress: Progress | None = progress if progress and isinstance(progress, Progress) else Progress()
        """The Rich Progress instance for displaying progress bars."""
        self._task_id: TaskID | None = self._progress.add_task(
                            description=self._description,
                            completed=completed,
                            total=total)
        """The Rich Progress TaskID for the task."""

    def start(self) -> None:
        """Start the task."""
        if self._progress is not None and self._task_id is not None:
            self._progress.start_task(self._task_id)

    def stop(self) -> None:
        """Stop the task."""
        if self._progress is not None and self._task_id is not None:
            self._progress.stop_task(self._task_id)

    def reset(self) -> None:
        """Reset the task progress."""
        if self._progress is not None and self._task_id is not None:
            self._progress.reset(self._task_id)

    def update(self, completed: int) -> None:
        """Update the task progress.

        Args:
            completed (int): The number of completed steps.
        """
        if not isinstance(completed, int):
            raise SimpleBenchTypeError(
                f'Expected completed arg to be an int, got {type(completed)}',
                ErrorTag.RICH_TASK_UPDATE_INVALID_COMPLETED_ARG)
        if self._progress is not None and self._task_id is not None:
            self._progress.update(task_id=self._task_id, completed=completed)
        else:
            raise SimpleBenchRuntimeError(
                'Task has already been terminated',
                ErrorTag.RICH_TASK_UPDATE_ALREADY_TERMINATED_TASK)

    def terminate_and_remove(self) -> None:
        """Terminate the task and remove it from the progress display."""
        if self._progress is not None and self._task_id is not None:
            self.stop()
            self._progress.update(task_id=self._task_id, visible=False)
            self._progress.remove_task(self._task_id)
            self._task_id = None
            self._progress = None
            raise SimpleBenchRuntimeError(
                'Task has already been terminated',
                ErrorTag.RICH_TASK_TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK)

class RichProgressTasks:
    """Task Rich Progress management for benchmarking."""
    def __init__(self) -> None:
        """Initialize a new RichProgressTasks instance."""
        self._progress = Progress()
        """The Rich Progress instance for displaying progress bars."""
        self._tasks: dict[str, RichTask] = {}
        """Mapping of task names to their RichTask instances."""

    def __contains__(self, task_name: str) -> bool:
        """Check if a task exists by name."""
        return task_name in self._tasks

    def __getitem__(self, name: str) -> RichTask:
        """Get a task by name.
        
        Example:

        task = progress_tasks['task_name']

        Args:
            name (str): The name of the task to retrieve.

        Returns:
            RichTask: The requested task.

        Raises:
            SimpleBenchKeyError: If the requested task does not exist.
        """
        if not isinstance(name, str):
            raise(SimpleBenchKeyError(
                'Key not found',
                ErrorTag.RICH_PROGRESS_TASK_GETITEM_INVALID_NAME_ARG))
        if name not in self._tasks:
            raise SimpleBenchKeyError(
                'Key not found',
                ErrorTag.RICH_PROGRESS_TASK_GETITEM_NOT_FOUND)
        return self._tasks[name]

    def __delitem__(self, name: str) -> None:
        """Delete a task by name from the internal task management.

        This causes the task to be terminated and removed from the managed index.

        Example:

        del progress_tasks['task_name']

        Args:
            name (str): The name of the task to delete.
        
        Raises:
            SimpleBenchKeyError: If the task does not exist.
        """
        if not isinstance(name, str):
            raise SimpleBenchTypeError(
                f'Expected name arg to be a str, got {type(name)}',
                ErrorTag.RICH_PROGRESS_TASK_DELITEM_INVALID_NAME_ARG)
                
        if name in self._tasks:
            task: RichTask = self._tasks[name]
            task.terminate_and_remove()
            del self._tasks[name]
        else:
            raise SimpleBenchKeyError(
                'Key not found',
                ErrorTag.RICH_PROGRESS_TASK_DELITEM_NOT_FOUND)

    def new_task(self,
                 name: str,
                 description: str,
                 total: int = 0,
                 completed: int = 0) -> RichTask:
        """Create a new RichTask.

        The new task is initialized with the given parameters,
        added to the task manager index, and a RichTask
        instance returned.

        The RichTask instance provides control over the task's progress and status.

        Args:
            name (str): The name of the task.
            description (str): The description of the task.
            total (int): The total number of steps for the task.
            completed (int): Number of steps completed (default = 0)

        Returns:
            RichTask: The created RichTask instance.
        """
        task: RichTask = RichTask(progress=self._progress,
                                  name=name,
                                  description=description,
                                  completed=completed,
                                  total=total)
        self._tasks[name] = task
        return task

    def get(self, name: str) -> RichTask | None:
        """Get a task by name or return None if not found.

        Args:
            name (str): The name of the task to retrieve.

        Returns:
            RichTask: The requested task, or None if not found.
        """
        if name in self._tasks:
            return self._tasks[name]
        return None