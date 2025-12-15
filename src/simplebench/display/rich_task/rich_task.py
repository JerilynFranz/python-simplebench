"""module for managing progress tasks using Rich Progress."""
from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.progress import Progress, Task, TaskID

from simplebench.enums import Verbosity
from simplebench.exceptions import SimpleBenchRuntimeError, SimpleBenchTypeError, SimpleBenchValueError

from ._error_tags import _RichTaskErrorTag


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

        :param name: The name of the task.
        :type name: str
        :param description: The description of the task.
        :type description: str
        :param completed: Completion step. Defaults to 0.
        :type completed: int, optional
        :param total: Total number of steps. Defaults to 100.
        :type total: int, optional
        :param progress: The Progress instance to use.
        :type progress: Progress
        :param verbosity: The verbosity level for console output.
        :type verbosity: Verbosity
        :raises SimpleBenchTypeError: If any argument is of an incorrect type.
        :raises SimpleBenchValueError: If any argument has an invalid value.
        """
        if not isinstance(name, str):
            raise SimpleBenchTypeError(
                f'Expected name arg are to be a str, got {type(name)}',
                tag=_RichTaskErrorTag.INIT_INVALID_NAME_ARG)
        if not name:
            raise SimpleBenchValueError(
                'name arg cannot be an empty string',
                tag=_RichTaskErrorTag.INIT_EMPTY_STRING_NAME)
        if not isinstance(description, str):
            raise SimpleBenchTypeError(
                f'Expected description arg to be a str, got {type(description)}',
                tag=_RichTaskErrorTag.INIT_INVALID_DESCRIPTION_ARG)
        if not description:
            raise SimpleBenchValueError(
                'description arg cannot be an empty string',
                tag=_RichTaskErrorTag.INIT_EMPTY_STRING_DESCRIPTION)
        if not isinstance(progress, Progress):
            raise SimpleBenchTypeError(
                f'Expected progress arg to be a Progress instance, got {type(progress)}',
                tag=_RichTaskErrorTag.INIT_INVALID_PROGRESS_ARG)

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

    def reset(self, start: bool = True) -> None:
        """Reset the task progress."""
        if self._progress is not None and self._task_id is not None:
            self._progress.reset(self._task_id, start=start)
            if self._verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Reset task '{self._name}' with ID {self._task_id}")

    def refresh(self) -> None:
        """Refresh the task progress display."""
        if self._progress is not None and self._task_id is not None:
            self._progress.refresh()
            if self._verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Refreshed task '{self._name}' with ID {self._task_id}")

    def update(self,
               completed: int | float | None = None,
               description: str | None = None,
               refresh: bool | None = None) -> None:
        """Update the task progress.

        If an attempt to update a terminated task is made, a
        :class:`~.exceptions.SimpleBenchRuntimeError` will be raised.

        :param completed: The number of completed steps.
        :type completed: int or float, optional
        :param description: The description of the task.
        :type description: str, optional
        :param refresh: Whether to refresh the progress display.
        :type refresh: bool, optional
        :raises SimpleBenchTypeError: If any argument is of an incorrect type.
        :raises SimpleBenchRuntimeError: If the task has already been terminated.
        """
        if completed is not None and not isinstance(completed, (int, float)):
            raise SimpleBenchTypeError(
                f'Expected completed arg to be an int or float, got {type(completed)}',
                tag=_RichTaskErrorTag.UPDATE_INVALID_COMPLETED_ARG)
        if description is not None and not isinstance(description, str):
            raise SimpleBenchTypeError(
                f'Expected description arg to be a str, got {type(description)}',
                tag=_RichTaskErrorTag.UPDATE_INVALID_DESCRIPTION_ARG)
        if refresh is not None and not isinstance(refresh, bool):
            raise SimpleBenchTypeError(
                f'Expected refresh arg to be a bool, got {type(refresh)}',
                tag=_RichTaskErrorTag.UPDATE_INVALID_REFRESH_ARG)
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
                tag=_RichTaskErrorTag.UPDATE_ALREADY_TERMINATED_TASK)

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
            tag=_RichTaskErrorTag.TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK)

    def get_task(self) -> Task | None:
        """Get the Rich Task instance from the Progress instance.

        :return: The Rich Task instance, or None if not found.
        :rtype: Task or None
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
