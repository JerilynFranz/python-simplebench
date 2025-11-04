"""TestSpec testing framework."""
from .assertions import Assert
from .base import TestSpec
from .constants import NO_EXPECTED_VALUE, NO_OBJ_ASSIGNED
from .context import Context
from .idspec import idspec
from .helpers import no_assigned_action
from .deferred import Deferred
from .test_action import TestAction
from .test_get import TestGet
from .test_set import TestSet
from .test_setget import TestSetGet

__test__ = False  # Prevent pytest from trying to collect this package as a test case

__all__ = [
    "NO_EXPECTED_VALUE",
    "NO_OBJ_ASSIGNED",
    "idspec",
    "no_assigned_action",
    "Assert",
    "Context",
    "Deferred",
    "TestAction",
    "TestGet",
    "TestSet",
    "TestSetGet",
    "TestSpec"
]
