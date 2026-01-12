"""module for managing progress tasks using Rich Progress."""

from __future__ import annotations

from rich.console import Console
from rich.progress import Progress

from simplebench.display.rich_task import RichTask
from simplebench.enums import Verbosity
from simplebench.exceptions import (
    SimpleBenchKeyError,
    SimpleBenchRuntimeError,
    SimpleBenchTypeError,
    SimpleBenchValueError,
)

from ._error_tags import _RichProgressTasksErrorTag


class RichProgressTasks:
    """Task Rich Progress management for benchmarking."""

    def __init__(self, verbosity: Verbosity, console: Console | None = None) -> None:
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
                tag=_RichProgressTasksErrorTag.INIT_INVALID_CONSOLE_ARG,
            )
        self._console: Console = console
        """The Rich Console instance for outputting messages."""
        self._progress = Progress(console=self._console, auto_refresh=True, transient=True, refresh_per_second=5)
        """The Rich Progress instance for displaying progress bars."""
        self._console = self._progress.console
        """The Rich Console instance for outputting messages."""
        self._tasks: dict[str, RichTask] = {}
        """Mapping of task names to their RichTask instances."""
        if not isinstance(verbosity, Verbosity):
            raise SimpleBenchTypeError(
                f'Expected verbosity arg to be a Verbosity enum, got {type(verbosity)}',
                tag=_RichProgressTasksErrorTag.INIT_INVALID_VERBOSITY_ARG,
            )
        self._verbosity: Verbosity = verbosity
        """The verbosity level for console output."""

        if self._verbosity >= Verbosity.DEBUG:
            self._console.print(f'[DEBUG] Initialized RichProgressTasks with verbosity {self._verbosity.name}')

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
            self._console.print('[DEBUG] Started Rich Progress display')

    def stop(self) -> None:
        """Stop the Rich Progress display."""
        self._progress.stop()
        self._is_running = False
        if self._verbosity >= Verbosity.DEBUG:
            self._console.print('[DEBUG] Stopped Rich Progress display')

    def clear(self) -> None:
        """Clear all tasks from the internal task management.

        This causes all tasks to be terminated and removed from the managed index.
        """
        for name in list(self._tasks.keys()):
            task: RichTask = self._tasks[name]
            try:
                task.terminate_and_remove()
            except SimpleBenchRuntimeError as e:
                self._console.print(f'[ERROR] Failed to terminate task {name}: {e}')
            del self._tasks[name]
        if self._verbosity >= Verbosity.DEBUG:
            self._console.print('[DEBUG] Cleared all tasks from RichProgressTasks')

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
            raise (SimpleBenchKeyError('Key not found', tag=_RichProgressTasksErrorTag.GETITEM_INVALID_NAME_ARG))
        if name not in self._tasks:
            raise SimpleBenchKeyError('Key not found', tag=_RichProgressTasksErrorTag.GETITEM_NOT_FOUND)
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
                tag=_RichProgressTasksErrorTag.DELITEM_INVALID_NAME_ARG,
            )

        if name in self._tasks:
            task: RichTask = self._tasks[name]
            task.terminate_and_remove()
            del self._tasks[name]
        else:
            raise SimpleBenchKeyError('Key not found', tag=_RichProgressTasksErrorTag.DELITEM_NOT_FOUND)

    def new_task(self, name: str, description: str, total: float = 0, completed: int = 0) -> RichTask:
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
        task: RichTask = RichTask(
            progress=self._progress,
            name=name,
            description=description,
            completed=completed,
            total=total,
            verbosity=self._verbosity,
        )
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
                f"Task with name '{name}' already exists.", tag=_RichProgressTasksErrorTag.ADD_TASK_DUPLICATE_NAME
            )

        task: RichTask = RichTask(
            progress=self._progress,
            name=name,
            description=description,
            completed=0,
            total=total,
            verbosity=self._verbosity,
        )
        self._tasks[name] = task
        return task
