"""Test for simplebench.types.values module."""
# ruff: noqa: E501
#import importlib.util  # Import the utility
#import sys
#from pathlib import Path

import autopypath  # noqa: F401 # autopypath adjusts sys.path on import when run as script
import pytest

# TODO: Think about adding a function to autopypath to load modules directly from file paths,
# bypassing the normal import system __init__.py files loading
# --- Definitive Workaround for circular import ---
# We cannot use `from simplebench...` as it loads the broken package.
# Instead, we load the `values.py` module directly from its file path.
## 1. Define the path to the module file.
#MODULE_PATH = Path(__file__).parent.parent.parent.parent / 'src' / 'simplebench' / 'simplebench_types' / '_values' / '_values.py'
#MODULE_NAME = 'simplebench.simplebench_types._values.values'
#
## 2. Use importlib to load the module from the path.
#spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
#if not spec or not spec.loader:
#    raise ImportError(f'Could not load spec for module at {MODULE_PATH}')
#
#values_module = importlib.util.module_from_spec(spec)
#sys.modules[MODULE_NAME] = values_module  # Add to sys.modules to make it discoverable
#spec.loader.exec_module(values_module)
## -----------------------------------------
#
## 3. Get the Values class from the dynamically loaded module.
#Values = values_module.Values
from testspec import Assert, TestSpec, PytestAction

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.simplebench_types import Values


@pytest.mark.parametrize(
    'testspec', [
        PytestAction('VALUES_001',
            name='Create Values instance from list of ints and floats',
            action=Values, args=[[1, 2.5, 3]],
            assertion=Assert.ISINSTANCE,
            expected=Values),
        PytestAction('VALUES_002',
            name='Create Values instance from empty list',
            action=Values, args=[[]],
            expected=Values()),
        PytestAction('VALUES_003',
            name='Validate Values contents are floats',
            action=Values, args=[[1, 2.5, 3]],
            validate_result=lambda result: all(isinstance(v, float) for v in result)),
        PytestAction('VALUES_004',
            name='Create Values instance with non-iterable (int) raises SimpleBenchTypeError',
            action=Values, args=[1],
            exception=SimpleBenchTypeError),
        PytestAction('VALUES_005',
            name='Create Values instance with non-numeric types raises TypeError',
            action=Values, args=[['a', None, 3]],
            exception=SimpleBenchTypeError),
        PytestAction('VALUES_006',
            name='Create Values instance is equivalent to tuple of floats',
            action=Values, args=[[1, 2.0, 3, 4.5]],
            expected=(1.0, 2.0, 3.0, 4.5)),
    ],
)
def test_values(testspec: TestSpec) -> None:
    """Test the Values class.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


if __name__ == '__main__':
    pytest.main([__file__])
