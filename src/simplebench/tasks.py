# -*- coding: utf-8 -*-
"""module for managing progress tasks using Rich Progress."""
from typing import Any, Optional

from rich.console import Console
from rich.progress import Progress, Task, TaskID

from .enums import Verbosity
from .exceptions import (SimpleBenchKeyError, SimpleBenchTypeError,
                         SimpleBenchValueError, SimpleBenchRuntimeError,
                         ErrorTag)


class RichTask:
    """Represents and controls a Rich Progress task."""
    def __init__(self,
                 progress: Progress,
                 name: str,
                 description: str,
                 completed: int = 0,
                 total: float = 100.0,
                 verbosity: Verbosity = Verbosity.NORMAL) -> None:
        """Construct a new RichTask.

        Args:
            name (str): The name of the task.
            description (str): The description of the task.
            completed (Optional[int]): Completion step (default=0)
            total (Optional[int]): Total number of steps (default=100)
            progress (Progress): The Progress instance to use.
            verbosity (Verbosity): The verbosity level for console output.

        Raises:
            SimpleBenchTypeError: If any argument is of an incorrect type.
            SimpleBenchValueError: If any argument has an invalid value.
        """
        if not isinstance(name, str):
            raise SimpleBenchTypeError(
                f'Expected name arg are to be a str, got {type(name)}',
                tag=ErrorTag.RICH_TASK_INIT_INVALID_NAME_ARG)
        if not name:
            raise SimpleBenchValueError(
                'name arg cannot be an empty string',
                tag=ErrorTag.RICH_TASK_INIT_EMPTY_STRING_NAME)
        if not isinstance(description, str):
            raise SimpleBenchTypeError(
                f'Expected description arg to be a str, got {type(description)}',
                tag=ErrorTag.RICH_TASK_INIT_INVALID_DESCRIPTION_ARG)
        if not description:
            raise SimpleBenchValueError(
                'description arg cannot be an empty string',
                tag=ErrorTag.RICH_TASK_INIT_EMPTY_STRING_DESCRIPTION)
        if not isinstance(progress, Progress):
            raise SimpleBenchTypeError(
                f'Expected progress arg to be a Progress instance, got {type(progress)}',
                tag=ErrorTag.RICH_TASK_INIT_INVALID_PROGRESS_ARG)

        self._name: str = name
        """The name of the task."""
        self._description: str = description
        """The description of the task."""
        self._verbosity: Verbosity = verbosity
        """The verbosity level for console output."""
        self._progress: Progress | None = progress
        """The Rich Progress instance for displaying progress bars."""
        self._console: Console = self._progress.console
        """The Rich Console instance for outputting messages."""
        self._task_id: TaskID | None = self._progress.add_task(
                            description=self._description,
                            completed=completed,
                            total=float(total),
                            start=True,
                            visible=True)
        """The Rich Progress TaskID for the new task."""
        if self._verbosity >= Verbosity.DEBUG:
            self._console.print(f"[DEBUG] Created task '{self._name}' with ID {self._task_id}")
        self.start()

    def start(self) -> None:
        """Start the task."""
        if self._progress is not None and self._task_id is not None:
            self._progress.start_task(self._task_id)
            if self._verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Started task '{self._name}' with ID {self._task_id}")

    def stop(self) -> None:
        """Stop the task."""
        if self._progress is not None and self._task_id is not None:
            self._progress.stop_task(self._task_id)

    def reset(self) -> None:
        """Reset the task progress."""
        if self._progress is not None and self._task_id is not None:
            self._progress.reset(self._task_id)
            if self._verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Reset task '{self._name}' with ID {self._task_id}")

    def refresh(self) -> None:
        """Refresh the task progress display."""
        if self._progress is not None and self._task_id is not None:
            self._progress.refresh()
            if self._verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Refreshed task '{self._name}' with ID {self._task_id}")

    def update(self,
               completed: Optional[int | float] = None,
               description: Optional[str] = None,
               refresh: Optional[bool] = None) -> None:
        """Update the task progress.

        If an attempt to update a terminated task is made, a
        SimpleBenchRuntimeError will be raised.

        Args:
            completed (int | float): The number of completed steps.
            description (Optional[str]): The description of the task.
            refresh (Optional[bool]): Whether to refresh the progress display.

        Raises:
            SimpleBenchTypeError: If any argument is of an incorrect type.
            SimpleBenchRuntimeError: If the task has already been terminated.
        """
        if completed is not None and not isinstance(completed, (int, float)):
            raise SimpleBenchTypeError(
                f'Expected completed arg to be an int or float, got {type(completed)}',
                tag=ErrorTag.RICH_TASK_UPDATE_INVALID_COMPLETED_ARG)
        if description is not None and not isinstance(description, str):
            raise SimpleBenchTypeError(
                f'Expected description arg to be a str, got {type(description)}',
                tag=ErrorTag.RICH_TASK_UPDATE_INVALID_DESCRIPTION_ARG)
        if refresh is not None and not isinstance(refresh, bool):
            raise SimpleBenchTypeError(
                f'Expected refresh arg to be a bool, got {type(refresh)}',
                tag=ErrorTag.RICH_TASK_UPDATE_INVALID_REFRESH_ARG)
        if self._progress is not None and self._task_id is not None:
            update_args: dict[str, Any] = {'task_id': self._task_id}

            if isinstance(description, str):
                update_args['description'] = description
            if isinstance(completed, (int, float)):
                update_args['completed'] = completed
            if isinstance(refresh, bool):
                update_args['refresh'] = refresh
            if update_args:
                self._progress.update(**update_args)
                if self._verbosity >= Verbosity.DEBUG:
                    self._console.print(f"[DEBUG] Updated task '{self._name}' with ID {self._task_id}: {update_args}")
        else:
            raise SimpleBenchRuntimeError(
                'Task has already been terminated',
                tag=ErrorTag.RICH_TASK_UPDATE_ALREADY_TERMINATED_TASK)

    def terminate_and_remove(self) -> None:
        """Terminate the task and remove it from the progress display."""
        if self._progress is not None and self._task_id is not None:
            self.stop()
            self._progress.update(task_id=self._task_id, visible=False)
            self._progress.remove_task(self._task_id)
            self._task_id = None
            self._progress = None
            if self._verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Terminated and removed task '{self._name}'")
            return
        # only reach here if task was previously terminated
        raise SimpleBenchRuntimeError(
            'Task has already been terminated',
            tag=ErrorTag.RICH_TASK_TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK)

    def get_task(self) -> Task | None:
        """Get the Rich Task instance from the Progress instance.

        Returns:
            Task: The Rich Task instance, or None if not found.
        """
        if self._progress is None or self._task_id is None:
            return None
        task_list: list[Task] = self._progress.tasks
        for task in task_list:
            if task.id == self._task_id:
                return task
        return None

    def __str__(self):
        """Return a string representation of the task."""
        return (f"RichTask(name='{self._name}', description='{self._description}', "
                f"task_id={self._task_id}, verbosity={self._verbosity.name}, task={self.get_task()})")


class RichProgressTasks:
    """Task Rich Progress management for benchmarking."""
    def __init__(self, verbosity: Verbosity, console: Optional[Console] = None) -> None:
        """Initialize a new RichProgressTasks instance.

        This instance manages multiple RichTask instances and provides
        a Rich Progress display for console output.

        The display will not start until the start() method is called on
        this instance.

        Args:
            verbosity (Verbosity): The verbosity level for console output.
            console (Optional[Console]): The Rich Console instance for displaying output.
                If None, a new Console will be created as needed. (default: None)
        Raises:
            SimpleBenchTypeError: If verbosity is not a Verbosity enum.
        """
        if console is None:
            console = Console()
        if not isinstance(console, Console):
            raise SimpleBenchTypeError(
                f'Expected console arg to be a Console instance, got {type(console)}',
                tag=ErrorTag.RICH_PROGRESS_TASKS_INIT_INVALID_CONSOLE_ARG)
        self._console: Console = console
        """The Rich Console instance for outputting messages."""
        self._progress = Progress(
            console=self._console,
            auto_refresh=True,
            transient=True,
            refresh_per_second=5
        )
        """The Rich Progress instance for displaying progress bars."""
        self._console = self._progress.console
        """The Rich Console instance for outputting messages."""
        self._tasks: dict[str, RichTask] = {}
        """Mapping of task names to their RichTask instances."""
        if not isinstance(verbosity, Verbosity):
            raise SimpleBenchTypeError(
                f'Expected verbosity arg to be a Verbosity enum, got {type(verbosity)}',
                tag=ErrorTag.RICH_PROGRESS_TASKS_INIT_INVALID_VERBOSITY_ARG)
        self._verbosity: Verbosity = verbosity
        """The verbosity level for console output."""

        if self._verbosity >= Verbosity.DEBUG:
            self._console.print(f"[DEBUG] Initialized RichProgressTasks with verbosity {self._verbosity.name}")

    def start(self) -> None:
        """Start the Rich Progress display."""
        self._progress.start()
        if self._verbosity >= Verbosity.DEBUG:
            self._console.print("[DEBUG] Started Rich Progress display")

    def stop(self) -> None:
        """Stop the Rich Progress display."""
        self._progress.stop()
        if self._verbosity >= Verbosity.DEBUG:
            self._console.print("[DEBUG] Stopped Rich Progress display")

    def clear(self) -> None:
        """Clear all tasks from the internal task management.

        This causes all tasks to be terminated and removed from the managed index.
        """
        for name in list(self._tasks.keys()):
            task: RichTask = self._tasks[name]
            try:
                task.terminate_and_remove()
            except SimpleBenchRuntimeError as e:
                self._console.print(f"[ERROR] Failed to terminate task {name}: {e}")
            del self._tasks[name]
        if self._verbosity >= Verbosity.DEBUG:
            self._console.print("[DEBUG] Cleared all tasks from RichProgressTasks")

        task_ids = self._progress.task_ids
        for task_id in task_ids:
            self._progress.remove_task(task_id)

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
            raise (SimpleBenchKeyError(
                'Key not found',
                tag=ErrorTag.RICH_PROGRESS_TASK_GETITEM_INVALID_NAME_ARG))
        if name not in self._tasks:
            raise SimpleBenchKeyError(
                'Key not found',
                tag=ErrorTag.RICH_PROGRESS_TASK_GETITEM_NOT_FOUND)
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
                tag=ErrorTag.RICH_PROGRESS_TASK_DELITEM_INVALID_NAME_ARG)

        if name in self._tasks:
            task: RichTask = self._tasks[name]
            task.terminate_and_remove()
            del self._tasks[name]
        else:
            raise SimpleBenchKeyError(
                'Key not found',
                tag=ErrorTag.RICH_PROGRESS_TASK_DELITEM_NOT_FOUND)

    def new_task(self,
                 name: str,
                 description: str,
                 total: float = 0,
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
                                  total=total,
                                  verbosity=self._verbosity)
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
