"""Tests for type hint validation functions."""
# pylint: disable=import-error,wrong-import-position,unused-import
import logging
import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

log = logging.getLogger(__name__)

# Automatically adjust sys.path to include src/ and tests/ directories for imports if needed.
# This lets us run the tests in this one file directly without first installing the package,
# depending on PYTHONPATH, or requiring a specific invocation of pytest to set up the import paths.
load_dotenv()
repo_markers = {
    'pyproject.toml': 'file',
    '.git': 'dir',
    '.hg': 'dir',
}
warn_on_mismatched_env_and_sep: bool = True
posix_pathsep = ':'
nt_pathsep = ';'
pathsep = os.pathsep
if warn_on_mismatched_env_and_sep:
    if os.name == 'nt' and posix_pathsep in os.getenv('PYTHONPATH', ''):
        log.warning("Detected POSIX-style path separator ':' in PYTHONPATH on Windows platform.")
    elif os.name != 'nt' and nt_pathsep in os.getenv('PYTHONPATH', ''):
        log.warning("Detected Windows-style path separator ';' in PYTHONPATH on POSIX platform.")

python_path_str = os.getenv('PYTHONPATH', '').strip()
subdirs_to_add = []
if python_path_str:
    log.debug("PYTHONPATH from environment: %s", python_path_str)
    normalized_path = python_path_str.replace(posix_pathsep, os.pathsep).replace(nt_pathsep, os.pathsep)
    subdirs_to_add = [p for p in normalized_path.split(os.pathsep) if p]

if subdirs_to_add:
    repo_root = Path(__file__).parent
    while not any((repo_root / marker).exists() if typ == 'file' else (repo_root / marker).is_dir()
                  for marker, typ in repo_markers.items()) and repo_root != repo_root.parent:
        repo_root = repo_root.parent
    if repo_root != repo_root.parent:
        for subdir in subdirs_to_add:
            subdir = Path(subdir.strip())
            candidate = repo_root / subdir
            if candidate.exists() and candidate.is_dir():
                if str(candidate) not in sys.path:
                    sys.path.insert(0, str(candidate))
            else:
                log.warning("Could not find expected subdirectory for imports: %s", candidate)
    else:
        log.warning("Could not find repository root for imports starting from: %s", Path(__file__))
else:
    log.warning("PYTHONPATH not set, imports may not work as expected.")

from testspec import Assert, TestAction, TestSpec, idspec

from simplebench.validators.type_hints import is_immutable_instance, isinstance_of_typehint
from simplebench.validators.type_hints._primitives import ImmutablePrimitiveTypes, ImmutablePrimitiveTypesTuple


@pytest.mark.parametrize('typespec', [
    idspec('IMMUTABLE_001', TestAction(
        name="Check immutable primitive: int",
        action=is_immutable_instance,
        args=[1, ImmutablePrimitiveTypes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('IMMUTABLE_002', TestAction(
        name="Check immutable primitive: float",
        action=is_immutable_instance,
        args=[3.14, ImmutablePrimitiveTypes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('IMMUTABLE_003', TestAction(
        name="Check immutable primitive: str",
        action=is_immutable_instance,
        args=["hello", ImmutablePrimitiveTypes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('IMMUTABLE_004', TestAction(
        name="Check immutable primitive: bool",
        action=is_immutable_instance,
        args=[True, ImmutablePrimitiveTypes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('IMMUTABLE_005', TestAction(
        name="Check immutable primitive: bytes",
        action=is_immutable_instance,
        args=[b'bytes', ImmutablePrimitiveTypes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('IMMUTABLE_006', TestAction(
        name="Check immutable primitive types: complex",
        action=is_immutable_instance,
        args=[complex(1, 2), ImmutablePrimitiveTypes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('IMMUTABLE_007', TestAction(
        name="Check immutable primitive: int",
        action=is_immutable_instance,
        args=[1, int],
        assertion=Assert.EQUAL,
        expected=True)),
])
def test_is_immutable(typespec: TestSpec) -> None:
    """Test is_instance_of_typehint function."""
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('TYPE_HINT_001', TestAction(
        name="Check immutable primitive: int",
        action=isinstance_of_typehint,
        args=[1, int],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_002', TestAction(
        name="Check immutable primitive value: str",
        action=isinstance_of_typehint,
        args=["hello", str],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_003', TestAction(
        name="Check immutable primitive value: bytes",
        action=isinstance_of_typehint,
        args=[b'bytes', bytes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_004', TestAction(
        name="Check immutable primitive value: bool",
        action=isinstance_of_typehint,
        args=[True, bool],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_005', TestAction(
        name="Check immutable primitive value: complex",
        action=isinstance_of_typehint,
        args=[complex(1, 2), complex],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_006', TestAction(
        name="Check immutable primitive value: float",
        action=isinstance_of_typehint,
        args=[3.14, float],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_007', TestAction(
        name="Check immutable primitive value: None)",
        action=isinstance_of_typehint,
        args=[None, None],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_008', TestAction(
        name="Check immutable primitive int value against union type hint (int | str)",
        action=isinstance_of_typehint,
        args=[1, int | str],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_009', TestAction(
        name="Check immutable primitive str value against union type hint (int | str)",
        action=isinstance_of_typehint,
        args=["test", int | str],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_0010', TestAction(
        name="Check immutable primitive float value against union type hint (float | bytes)",
        action=isinstance_of_typehint,
        args=[2.71, float | bytes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('TYPE_HINT_011', TestAction(
        name="Check immutable primitive bytes value against union type hint (float | bytes)",
        action=isinstance_of_typehint,
        args=[b'data', float | bytes],
        assertion=Assert.EQUAL,
        expected=True)),
])
def test_is_instance_of_typehint(typespec: TestSpec) -> None:
    """Test is_instance_of_typehint function."""
    typespec.run()


if __name__ == '__main__':
    pytest.main([__file__, "--log-cli-level=DEBUG", '-s'])
