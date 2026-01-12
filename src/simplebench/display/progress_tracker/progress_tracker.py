"""module for managing progress tasks using Rich Progress."""

from __future__ import annotations

from typing import TYPE_CHECKING

from simplebench.enums import Color, Verbosity

if TYPE_CHECKING:
    from simplebench.display.rich_task import RichTask
    from simplebench.session import Session


class ProgressTracker:
    """Helper to manage benchmark progress updates."""

    def __init__(
        self,
        *,
        session: Session | None = None,
        task_name: str,
        progress_max: int | float = 100,
        description: str = 'Benchmarking',
        color: Color = Color.GREEN,
    ) -> None:
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

        if (
            self._session
            and self._session.show_progress
            and self._session.verbosity > Verbosity.QUIET
            and self._session.tasks
        ):
            self._task = self._session.tasks.get(task_name)
            if not self._task:
                self._task = self._session.tasks.new_task(
                    name=task_name, description=self.styled_description, completed=0, total=progress_max
                )
        if self._task:
            self._task.reset()
            self._task.update(completed=5, description=self.styled_description)

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

    def update(
        self, completed: int | float, description: str, refresh: bool | None = None, color: Color | None = None
    ) -> None:
        """Update progress display."""
        if description:
            self._description = description
        if color is not None:
            self._color = color
        if self._task:
            self._task.update(completed=completed, description=self.styled_description, refresh=refresh)

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
