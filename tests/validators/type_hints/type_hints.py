"""Tests for type hint validation functions."""
# pylint: disable=import-error,wrong-import-position,unused-import
import logging
import os
import sys
from collections.abc import Iterable, Mapping, Sequence, Set
from pathlib import Path
from types import MappingProxyType, NoneType
from typing import Annotated, Any, Literal

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

from simplebench.validators.type_hints import clear_typehint_cache, isinstance_of_typehint
from simplebench.validators.type_hints._primitives import ImmutablePrimitiveTypes, ImmutablePrimitiveTypesTuple


@pytest.mark.parametrize('typespec', [
    idspec('PRIMITIVES_001', TestAction(
        name="1 is a int",
        action=isinstance_of_typehint,
        args=[1, int],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_002', TestAction(
        name="'hello' is a str",
        action=isinstance_of_typehint,
        args=["hello", str],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_003', TestAction(
        name="b'bytes' is a bytes",
        action=isinstance_of_typehint,
        args=[b'bytes', bytes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_004', TestAction(
        name="True is a bool",
        action=isinstance_of_typehint,
        args=[True, bool],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_005', TestAction(
        name="complex(1, 2) is a complex",
        action=isinstance_of_typehint,
        args=[complex(1, 2), complex],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_006', TestAction(
        name="3.14 is a float",
        action=isinstance_of_typehint,
        args=[3.14, float],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_007', TestAction(
        name="None is a None",
        action=isinstance_of_typehint,
        args=[None, None],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_008', TestAction(
        name="None is a NoneType",
        action=isinstance_of_typehint,
        args=[None, type(None)],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_009', TestAction(
        name="3 is not a str",
        action=isinstance_of_typehint,
        args=[3, str],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('PRIMITIVES_010', TestAction(
        name="'hello' is not a bytes",
        action=isinstance_of_typehint,
        args=["hello", bytes],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('PRIMITIVES_011', TestAction(
        name="b'bytes' is not a str",
        action=isinstance_of_typehint,
        args=[b'bytes', str],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('PRIMITIVES_012', TestAction(  # Wierd true fact!
        name="True is an int",
        action=isinstance_of_typehint,
        args=[True, int],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_013', TestAction(
        name="complex(1, 2) is not a float",
        action=isinstance_of_typehint,
        args=[complex(1, 2), float],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('PRIMITIVES_014', TestAction(
        name="3.14 is not an int",
        action=isinstance_of_typehint,
        args=[3.14, int],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('PRIMITIVES_015', TestAction(
        name="None is not an int",
        action=isinstance_of_typehint,
        args=[None, int],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('PRIMITIVES_016', TestAction(
        name="1 is an Any",
        action=isinstance_of_typehint,
        args=[1, Any],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_017', TestAction(
        name="'string' is an Any",
        action=isinstance_of_typehint,
        args=["string", Any],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_018', TestAction(
        name="b'bytes' is an Any",
        action=isinstance_of_typehint,
        args=[b'bytes', Any],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_019', TestAction(
        name="True is an Any",
        action=isinstance_of_typehint,
        args=[True, Any],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_020', TestAction(
        name="3.14 is an Any",
        action=isinstance_of_typehint,
        args=[3.14, Any],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_021', TestAction(
        name="None is an Any",
        action=isinstance_of_typehint,
        args=[None, Any],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_022', TestAction(
        name="1 is an object",
        action=isinstance_of_typehint,
        args=[1, object],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_023', TestAction(
        name="'string' is an object",
        action=isinstance_of_typehint,
        args=["string", object],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_024', TestAction(
        name="b'bytes' is an object",
        action=isinstance_of_typehint,
        args=[b'bytes', object],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_025', TestAction(
        name="True is an object",
        action=isinstance_of_typehint,
        args=[True, object],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_026', TestAction(
        name="3.14 is an object",
        action=isinstance_of_typehint,
        args=[3.14, object],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_027', TestAction(
        name="None is an object",
        action=isinstance_of_typehint,
        args=[None, object],
        assertion=Assert.EQUAL,
        expected=True)),
])
def test_primitives(typespec: TestSpec) -> None:
    """Test primitives."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('LITERALS_001', TestAction(
        name="1 is Literal[1]",
        action=isinstance_of_typehint,
        args=[1, Literal[1]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('LITERALS_002', TestAction(
        name="'hello' is Literal['hello']",
        action=isinstance_of_typehint,
        args=["hello", Literal['hello']],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('LITERALS_003', TestAction(
        name="b'bytes' is Literal[b'bytes']",
        action=isinstance_of_typehint,
        args=[b'bytes', Literal[b'bytes']],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('LITERALS_004', TestAction(
        name="True is Literal[True]",
        action=isinstance_of_typehint,
        args=[True, Literal[True]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('LITERALS_005', TestAction(
        name="3.14 is Literal[3.14]",
        action=isinstance_of_typehint,
        args=[3.14, Literal[3.14]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('LITERALS_006', TestAction(
        name="1 is not Literal[2]",
        action=isinstance_of_typehint,
        args=[1, Literal[2]],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('LITERALS_007', TestAction(
        name="'hello' is not Literal['world']",
        action=isinstance_of_typehint,
        args=["hello", Literal['world']],
        assertion=Assert.EQUAL,
        expected=False)),
])
def test_literals(typespec: TestSpec) -> None:
    """Test literals."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('UNIONS_001', TestAction(
        name="1 is a int | str",
        action=isinstance_of_typehint,
        args=[1, int | str],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('UNIONS_002', TestAction(
        name="'test' is a int | str",
        action=isinstance_of_typehint,
        args=["test", int | str],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('UNIONS_003', TestAction(
        name="2.71 is a float | bytes",
        action=isinstance_of_typehint,
        args=[2.71, float | bytes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('UNIONS_004', TestAction(
        name="b'data' is a float | bytes",
        action=isinstance_of_typehint,
        args=[b'data', float | bytes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('UNIONS_005', TestAction(
        name="False is a bool | None",
        action=isinstance_of_typehint,
        args=[False, bool | None],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('UNIONS_006', TestAction(
        name="None is a bool | None",
        action=isinstance_of_typehint,
        args=[None, bool | None],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('UNIONS_007', TestAction(
        name="3+4j is a complex | int",
        action=isinstance_of_typehint,
        args=[3+4j, complex | int],
        assertion=Assert.EQUAL,
        expected=True)),
])
def test_unions(typespec: TestSpec) -> None:
    """Test unions."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('ANNOTATED_001', TestAction(
        name="1 is Annotated[int, 'metadata']",
        action=isinstance_of_typehint,
        args=[1, Annotated[int, 'metadata']],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ANNOTATED_002', TestAction(
        name="'a' is not Annotated[int, 'metadata']",
        action=isinstance_of_typehint,
        args=['a', Annotated[int, 'metadata']],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('ANNOTATED_003', TestAction(
        name="'a' is Annotated[str | int, 'metadata']",
        action=isinstance_of_typehint,
        args=['a', Annotated[str | int, 'metadata']],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ANNOTATED_004', TestAction(
        name="1 is Annotated[str | int, 'metadata']",
        action=isinstance_of_typehint,
        args=[1, Annotated[str | int, 'metadata']],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ANNOTATED_005', TestAction(
        name="None is Annotated[None, 'metadata']",
        action=isinstance_of_typehint,
        args=[None, Annotated[None, 'metadata']],
        assertion=Assert.EQUAL,
        expected=True)),
])
def test_annotated(typespec: TestSpec) -> None:
    """Test annotated types."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('SETS_001', TestAction(
        name="{1, 2} is a set",
        action=isinstance_of_typehint,
        args=[{1, 2}, set],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SETS_002', TestAction(
        name="{1, 2} is a set[int]",
        action=isinstance_of_typehint,
        args=[{1, 2}, set[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SETS_003', TestAction(
        name="{1, 'a'} is a set[int | str]",
        action=isinstance_of_typehint,
        args=[{1, 'a'}, set[int | str]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SETS_004', TestAction(
        name="{1, 2} is not a set[str]",
        action=isinstance_of_typehint,
        args=[{1, 2}, set[str]],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('SETS_005', TestAction(
        name="empty set is a set[int]",
        action=isinstance_of_typehint,
        args=[set(), set[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SETS_006', TestAction(
        name="{1, 2} is a collections.abc.Set",
        action=isinstance_of_typehint,
        args=[{1, 2}, Set],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SETS_007', TestAction(
        name="{1, 2} is a collections.abc.Set[int]",
        action=isinstance_of_typehint,
        args=[{1, 2}, Set[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SETS_008', TestAction(
        name="frozenset({1, 2}) is a frozenset[int]",
        action=isinstance_of_typehint,
        args=[frozenset({1, 2}), frozenset[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SETS_009', TestAction(
        name="frozenset({1, 2}) is not a set[int]",
        action=isinstance_of_typehint,
        args=[frozenset({1, 2}), set[int]],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('SETS_010', TestAction(
        name="frozenset({1, 2}) is a collections.abc.Set[int]",
        action=isinstance_of_typehint,
        args=[frozenset({1, 2}), Set[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SETS_011', TestAction(
        name="[1, 2] is not a set[int]",
        action=isinstance_of_typehint,
        args=[[1, 2], set[int]],
        assertion=Assert.EQUAL,
        expected=False)),
])
def test_sets(typespec: TestSpec) -> None:
    """Test set types."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('MAPPINGS_001', TestAction(
        name="{'a': 1} is a dict",
        action=isinstance_of_typehint,
        args=[{'a': 1}, dict],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('MAPPINGS_002', TestAction(
        name="{'a': 1} is a dict[str, int]",
        action=isinstance_of_typehint,
        args=[{'a': 1}, dict[str, int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('MAPPINGS_003', TestAction(
        name="{'a': 1, 'b': 'c'} is a dict[str, int | str]",
        action=isinstance_of_typehint,
        args=[{'a': 1, 'b': 'c'}, dict[str, int | str]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('MAPPINGS_004', TestAction(
        name="{'a': 1} is not a dict[str, str]",
        action=isinstance_of_typehint,
        args=[{'a': 1}, dict[str, str]],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('MAPPINGS_005', TestAction(
        name="{'a': 1} is not a dict[int, int]",
        action=isinstance_of_typehint,
        args=[{'a': 1}, dict[int, int]],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('MAPPINGS_006', TestAction(
        name="empty dict is a dict[str, int]",
        action=isinstance_of_typehint,
        args=[{}, dict[str, int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('MAPPINGS_007', TestAction(
        name="{'a': 1} is a Mapping",
        action=isinstance_of_typehint,
        args=[{'a': 1}, Mapping],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('MAPPINGS_008', TestAction(
        name="{'a': 1} is a Mapping[str, int]",
        action=isinstance_of_typehint,
        args=[{'a': 1}, Mapping[str, int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('MAPPINGS_009', TestAction(
        name="MappingProxyType is a Mapping[str, int]",
        action=isinstance_of_typehint,
        args=[MappingProxyType({'a': 1}), Mapping[str, int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('MAPPINGS_010', TestAction(
        name="{'a': {'b': 1}} is a dict[str, dict[str, int]]",
        action=isinstance_of_typehint,
        args=[{'a': {'b': 1}}, dict[str, dict[str, int]]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('MAPPINGS_011', TestAction(
        name="{'a': {'b': 1}} is not a dict[str, dict[str, str]]",
        action=isinstance_of_typehint,
        args=[{'a': {'b': 1}}, dict[str, dict[str, str]]],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('MAPPINGS_012', TestAction(
        name="[1, 2] is not a dict",
        action=isinstance_of_typehint,
        args=[[1, 2], dict],
        assertion=Assert.EQUAL,
        expected=False)),
])
def test_mappings(typespec: TestSpec) -> None:
    """Test mapping types."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('SEQUENCES_001', TestAction(
        name="[1, 2] is a list",
        action=isinstance_of_typehint,
        args=[[1, 2], list],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SEQUENCES_002', TestAction(
        name="[1, 2] is a list[int]",
        action=isinstance_of_typehint,
        args=[[1, 2], list[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SEQUENCES_003', TestAction(
        name="[1, 'a'] is a list[int | str]",
        action=isinstance_of_typehint,
        args=[[1, 'a'], list[int | str]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SEQUENCES_004', TestAction(
        name="[1, 2] is not a list[str]",
        action=isinstance_of_typehint,
        args=[[1, 2], list[str]],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('SEQUENCES_005', TestAction(
        name="empty list is a list[int]",
        action=isinstance_of_typehint,
        args=[[], list[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SEQUENCES_006', TestAction(
        name="[1, 2] is a collections.abc.Sequence",
        action=isinstance_of_typehint,
        args=[[1, 2], Sequence],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SEQUENCES_007', TestAction(
        name="[1, 2] is a collections.abc.Sequence[int]",
        action=isinstance_of_typehint,
        args=[[1, 2], Sequence[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SEQUENCES_008', TestAction(
        name="(1, 2) is a tuple[int, int]",
        action=isinstance_of_typehint,
        args=[(1, 2), tuple[int, int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SEQUENCES_009', TestAction(
        name="(1, 2) is a collections.abc.Sequence[int]",
        action=isinstance_of_typehint,
        args=[(1, 2), Sequence[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SEQUENCES_010', TestAction(
        name="[[1], [2]] is a list[list[int]]",
        action=isinstance_of_typehint,
        args=[[[1], [2]], list[list[int]]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('SEQUENCES_011', TestAction(
        name="[[1], [2]] is not a list[list[str]]",
        action=isinstance_of_typehint,
        args=[[[1], [2]], list[list[str]]],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('SEQUENCES_012', TestAction(
        name="{'a': 1} is not a list",
        action=isinstance_of_typehint,
        args=[{'a': 1}, list],
        assertion=Assert.EQUAL,
        expected=False)),
])
def test_sequences(typespec: TestSpec) -> None:
    """Test sequence types."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('ITERABLES_001', TestAction(
        name="[1, 2] is an Iterable",
        action=isinstance_of_typehint,
        args=[[1, 2], Iterable],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ITERABLES_002', TestAction(
        name="[1, 2] is an Iterable[int]",
        action=isinstance_of_typehint,
        args=[[1, 2], Iterable[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ITERABLES_003', TestAction(
        name="{1, 2} is an Iterable[int]",
        action=isinstance_of_typehint,
        args=[{1, 2}, Iterable[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ITERABLES_004', TestAction(
        name="(1, 2) is an Iterable[int]",
        action=isinstance_of_typehint,
        args=[(1, 2), Iterable[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ITERABLES_005', TestAction(
        name="'abc' is an Iterable[str]",
        action=isinstance_of_typehint,
        args=['abc', Iterable[str]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ITERABLES_006', TestAction(
        name="b'abc' is an Iterable[int]",
        action=isinstance_of_typehint,
        args=[b'abc', Iterable[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ITERABLES_007', TestAction(
        name="{'a': 1} is an Iterable[str] (keys)",
        action=isinstance_of_typehint,
        args=[{'a': 1}, Iterable[str]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ITERABLES_008', TestAction(
        name="[1, 2] is not an Iterable[str]",
        action=isinstance_of_typehint,
        args=[[1, 2], Iterable[str]],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('ITERABLES_009', TestAction(
        name="empty list is an Iterable[int]",
        action=isinstance_of_typehint,
        args=[[], Iterable[int]],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ITERABLES_010', TestAction(
        name="123 is not an Iterable",
        action=isinstance_of_typehint,
        args=[123, Iterable],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('ITERABLES_011', TestAction(
        name="generator is an Iterable[int]",
        action=isinstance_of_typehint,
        args=[(i for i in range(3)), Iterable[int]],
        kwargs={'consume_iterators': True},
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('ITERABLES_012', TestAction(
        name="generator is not an Iterable[str]",
        action=isinstance_of_typehint,
        args=[(i for i in range(3)), Iterable[str]],
        kwargs={'consume_iterators': True},
        assertion=Assert.EQUAL,
        expected=False)),
])
def test_iterables(typespec: TestSpec) -> None:
    """Test iterable types."""
    clear_typehint_cache()
    typespec.run()



if __name__ == '__main__':
    pytest.main([__file__, "--log-cli-level=INFO", '-s'])
