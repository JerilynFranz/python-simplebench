# -*- coding: utf-8 -*-
"""module for managing progress tasks using Rich Progress."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from rich.console import Console
from rich.progress import Progress, Task, TaskID

from .enums import Color, Verbosity
from .exceptions import SimpleBenchKeyError, SimpleBenchRuntimeError, SimpleBenchTypeError, SimpleBenchValueError
from .exceptions.tasks import RichProgressTasksErrorTag, RichTaskErrorTag

if TYPE_CHECKING:
    from .session import Session


class ProgressTracker:
    """Helper to manage benchmark progress updates."""

    def __init__(self, *,
                 session: Session | None = None,
                 task_name: str,
                 progress_max: int | float = 100,
                 description: str = 'Benchmarking',
                 color: Color = Color.GREEN) -> None:
        """Initialize the ProgressTracker.

        :param session: The Session instance.
        :type session: Session or None
        :param task_name: The name of the progress task.
        :type task_name: str
        :param progress_max: The maximum value for progress completion.
            Defaults to 100.
        :type progress_max: int or float, optional
        :param description: The description for the progress task.
            Defaults to 'Benchmarking'.
        :type description: str, optional
        :param color: The color for the progress task.
            Defaults to :attr:`~.enums.Color.GREEN`.
        :type color: Color, optional
        """
        self._session: Session | None = session
        self._task: RichTask | None = None
        self._color: Color = color
        self._is_running: bool = False
        self._description: str = description

        if (self._session and self._session.show_progress
                and self._session.verbosity > Verbosity.QUIET and self._session.tasks):
            self._task = self._session.tasks.get(task_name)
            if not self._task:
                self._task = self._session.tasks.new_task(
                    name=task_name,
                    description=self.styled_description,
                    completed=0,
                    total=progress_max)
        if self._task:
            self._task.reset()
            self._task.update(
                completed=5,
                description=self.styled_description)

    @property
    def styled_description(self) -> str:
        """Get the styled description for the progress task."""
        return f'[{self._color.value}]{self._description}[/ {self._color.value}]'

    @property
    def is_running(self) -> bool:
        """Check if the Rich Progress display is currently running.

        :return: True if the display is running, False otherwise.
        :rtype: bool
        """
        return self._is_running

    def update(self,
               completed: int | float,
               description: str,
               refresh: bool | None = None,
               color: Color | None = None) -> None:
        """Update progress display."""
        if description:
            self._description = description
        if color is not None:
            self._color = color
        if self._task:
            self._task.update(
                completed=completed,
                description=self.styled_description,
                refresh=refresh)

    def start(self) -> None:
        """Start the progress tracking."""
        if self._task and self._session and self._session.tasks.is_running:
            self._task.start()
            self._is_running = True

    def stop(self) -> None:
        """Stop the progress tracking."""
        if self._task and self.is_running:
            self._task.stop()
            self._is_running = False

    def refresh(self) -> None:
        """Refresh the progress tracking display."""
        if self._task:
            self._task.refresh()

    def reset(self, start: bool = True) -> None:
        """Reset the progress tracking.

        This will reset the progress completion to zero and start it running by default.

        :param start: Whether to start the progress tracking after resetting.
            Defaults to True.
        :type start: bool, optional
        """
        if self._task:
            self._task.reset(start=start)
            self._is_running = start


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
                tag=RichTaskErrorTag.INIT_INVALID_NAME_ARG)
        if not name:
            raise SimpleBenchValueError(
                'name arg cannot be an empty string',
                tag=RichTaskErrorTag.INIT_EMPTY_STRING_NAME)
        if not isinstance(description, str):
            raise SimpleBenchTypeError(
                f'Expected description arg to be a str, got {type(description)}',
                tag=RichTaskErrorTag.INIT_INVALID_DESCRIPTION_ARG)
        if not description:
            raise SimpleBenchValueError(
                'description arg cannot be an empty string',
                tag=RichTaskErrorTag.INIT_EMPTY_STRING_DESCRIPTION)
        if not isinstance(progress, Progress):
            raise SimpleBenchTypeError(
                f'Expected progress arg to be a Progress instance, got {type(progress)}',
                tag=RichTaskErrorTag.INIT_INVALID_PROGRESS_ARG)

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
                tag=RichTaskErrorTag.UPDATE_INVALID_COMPLETED_ARG)
        if description is not None and not isinstance(description, str):
            raise SimpleBenchTypeError(
                f'Expected description arg to be a str, got {type(description)}',
                tag=RichTaskErrorTag.UPDATE_INVALID_DESCRIPTION_ARG)
        if refresh is not None and not isinstance(refresh, bool):
            raise SimpleBenchTypeError(
                f'Expected refresh arg to be a bool, got {type(refresh)}',
                tag=RichTaskErrorTag.UPDATE_INVALID_REFRESH_ARG)
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
                tag=RichTaskErrorTag.UPDATE_ALREADY_TERMINATED_TASK)

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
            tag=RichTaskErrorTag.TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK)

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


class RichProgressTasks:
    """Task Rich Progress management for benchmarking."""
    def __init__(self, verbosity: Verbosity, console: Optional[Console] = None) -> None:
        """Initialize a new RichProgressTasks instance.

        This instance manages multiple :class:`RichTask` instances and provides
        a Rich Progress display for console output.

        The display will not start until the :meth:`start` method is called on
        this instance.

        :param verbosity: The verbosity level for console output.
        :type verbosity: Verbosity
        :param console: The Rich Console instance for displaying output.
            If None, a new Console will be created as needed. Defaults to None.
        :type console: Console, optional
        :raises SimpleBenchTypeError: If ``verbosity`` is not a :class:`~.enums.Verbosity` enum.
        """
        if console is None:
            console = Console()
        if not isinstance(console, Console):
            raise SimpleBenchTypeError(
                f'Expected console arg to be a Console instance, got {type(console)}',
                tag=RichProgressTasksErrorTag.INIT_INVALID_CONSOLE_ARG)
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
                tag=RichProgressTasksErrorTag.INIT_INVALID_VERBOSITY_ARG)
        self._verbosity: Verbosity = verbosity
        """The verbosity level for console output."""

        if self._verbosity >= Verbosity.DEBUG:
            self._console.print(f"[DEBUG] Initialized RichProgressTasks with verbosity {self._verbosity.name}")

        self._is_running: bool = False
        """Indicates whether the Rich Progress display is running (has been started but not stopped)."""

    @property
    def progress(self) -> Progress:
        """Get the Rich Progress instance."""
        return self._progress

    @property
    def is_running(self) -> bool:
        """If the Rich Progress display is currently running.

        The display is considered running if the start() method has been called
        and the stop() method has not yet been called.

        Value is True if running, False otherwise.
        """
        return self._is_running

    def start(self) -> None:
        """Start the Rich Progress display."""
        self._progress.start()
        self._is_running = True
        if self._verbosity >= Verbosity.DEBUG:
            self._console.print("[DEBUG] Started Rich Progress display")

    def stop(self) -> None:
        """Stop the Rich Progress display."""
        self._progress.stop()
        self._is_running = False
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

        .. code-block:: python

            task = progress_tasks['task_name']

        :param name: The name of the task to retrieve.
        :type name: str
        :raises SimpleBenchKeyError: If the requested task does not exist.
        :return: The requested task.
        :rtype: RichTask
        """
        if not isinstance(name, str):
            raise (SimpleBenchKeyError(
                'Key not found',
                tag=RichProgressTasksErrorTag.GETITEM_INVALID_NAME_ARG))
        if name not in self._tasks:
            raise SimpleBenchKeyError(
                'Key not found',
                tag=RichProgressTasksErrorTag.GETITEM_NOT_FOUND)
        return self._tasks[name]

    def __delitem__(self, name: str) -> None:
        """Delete a task by name from the internal task management.

        This causes the task to be terminated and removed from the managed index.

        Example:

        .. code-block:: python

            del progress_tasks['task_name']

        :param name: The name of the task to delete.
        :type name: str
        :raises SimpleBenchKeyError: If the task does not exist.
        """
        if not isinstance(name, str):
            raise SimpleBenchTypeError(
                f'Expected name arg to be a str, got {type(name)}',
                tag=RichProgressTasksErrorTag.DELITEM_INVALID_NAME_ARG)

        if name in self._tasks:
            task: RichTask = self._tasks[name]
            task.terminate_and_remove()
            del self._tasks[name]
        else:
            raise SimpleBenchKeyError(
                'Key not found',
                tag=RichProgressTasksErrorTag.DELITEM_NOT_FOUND)

    def new_task(self,
                 name: str,
                 description: str,
                 total: float = 0,
                 completed: int = 0) -> RichTask:
        """Create a new RichTask.

        The new task is initialized with the given parameters,
        added to the task manager index, and a :class:`RichTask`
        instance returned.

        The :class:`RichTask` instance provides control over the task's progress and status.

        :param name: The name of the task.
        :type name: str
        :param description: The description of the task.
        :type description: str
        :param total: The total number of steps for the task.
        :type total: int
        :param completed: Number of steps completed. Defaults to 0.
        :type completed: int, optional
        :return: The created RichTask instance.
        :rtype: RichTask
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

        :param name: The name of the task to retrieve.
        :type name: str
        :return: The requested task, or None if not found.
        :rtype: RichTask or None
        """
        if name in self._tasks:
            return self._tasks[name]
        return None

    def add_task(self, name: str, description: str, total: float = 100.0) -> RichTask:
        """Add a new task to the Rich Progress display.

        If a task with the same name already exists, a :exc:`~.exceptions.SimpleBenchValueError`
        is raised.

        :param name: The unique name for the task.
        :type name: str
        :param description: The description to display for the task.
        :type description: str
        :param total: The total number of steps for the task. Defaults to 100.0.
        :type total: float
        :raises SimpleBenchValueError: If a task with the same name already exists.
        :return: The newly created RichTask instance.
        :rtype: RichTask
        """
        if name in self._tasks:
            raise SimpleBenchValueError(
                f"Task with name '{name}' already exists.",
                tag=RichProgressTasksErrorTag.ADD_TASK_DUPLICATE_NAME)

        task: RichTask = RichTask(progress=self._progress,
                                  name=name,
                                  description=description,
                                  completed=0,
                                  total=total,
                                  verbosity=self._verbosity)
        self._tasks[name] = task
        return task
