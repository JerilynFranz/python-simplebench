"""Protocols for SimpleBench."""
from typing import Protocol, runtime_checkable

from .results import Results
from .runners import SimpleRunner


@runtime_checkable
class ActionRunner(Protocol):
    """A protocol for benchmark action functions used by Case."""
    def __call__(self, bench: SimpleRunner, **kwargs) -> Results:
        ...
