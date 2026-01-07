"""Tests for type hint validation functions."""
# pylint: disable=import-error,wrong-import-position,unused-import
import enum
import logging
import os
import sys
from collections.abc import Collection, Hashable, Iterable, Mapping, Sequence, Set
from pathlib import Path
from types import MappingProxyType
from typing import Annotated, Any, Callable, Final, Literal, NewType, Protocol, TypedDict, runtime_checkable

import pytest
from dotenv import load_dotenv

if sys.version_info >= (3, 11):
    from typing import Never, NotRequired, ReadOnly, Required
else:
    try:
        from typing_extensions import Never, NotRequired, ReadOnly, Required
    except ImportError as e:
        raise ImportError(
            "SimpleBench requires 'typing_extensions' for Python < 3.11 "
            "to support Never.") from e


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
        action=isinstance_of_typehint, args=[1, int],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_002', TestAction(
        name="'hello' is a str",
        action=isinstance_of_typehint, args=["hello", str],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_003', TestAction(
        name="b'bytes' is a bytes",
        action=isinstance_of_typehint, args=[b'bytes', bytes],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_004', TestAction(
        name="True is a bool",
        action=isinstance_of_typehint, args=[True, bool],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_005', TestAction(
        name="complex(1, 2) is a complex",
        action=isinstance_of_typehint, args=[complex(1, 2), complex],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_006', TestAction(
        name="3.14 is a float",
        action=isinstance_of_typehint, args=[3.14, float],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_007', TestAction(
        name="None is a None",
        action=isinstance_of_typehint, args=[None, None],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_008', TestAction(
        name="None is a NoneType",
        action=isinstance_of_typehint, args=[None, type(None)],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_009', TestAction(
        name="3 is not a str",
        action=isinstance_of_typehint, args=[3, str],
        assertion=Assert.FALSE)),
    idspec('PRIMITIVES_010', TestAction(
        name="'hello' is not a bytes",
        action=isinstance_of_typehint, args=["hello", bytes],
        assertion=Assert.FALSE)),
    idspec('PRIMITIVES_011', TestAction(
        name="b'bytes' is not a str",
        action=isinstance_of_typehint, args=[b'bytes', str],
        assertion=Assert.FALSE)),
    idspec('PRIMITIVES_012', TestAction(  # Wierd true fact!
        name="True is an int",
        action=isinstance_of_typehint, args=[True, int],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_013', TestAction(
        name="complex(1, 2) is not a float",
        action=isinstance_of_typehint, args=[complex(1, 2), float],
        assertion=Assert.FALSE)),
    idspec('PRIMITIVES_014', TestAction(
        name="3.14 is not an int",
        action=isinstance_of_typehint, args=[3.14, int],
        assertion=Assert.FALSE)),
    idspec('PRIMITIVES_015', TestAction(
        name="None is not an int",
        action=isinstance_of_typehint,
        args=[None, int],
        assertion=Assert.EQUAL,
        expected=False)),
    idspec('PRIMITIVES_016', TestAction(
        name="1 is an Any",
        action=isinstance_of_typehint, args=[1, Any],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_017', TestAction(
        name="'string' is an Any",
        action=isinstance_of_typehint, args=["string", Any],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_018', TestAction(
        name="b'bytes' is an Any",
        action=isinstance_of_typehint,
        args=[b'bytes', Any],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('PRIMITIVES_019', TestAction(
        name="True is an Any",
        action=isinstance_of_typehint, args=[True, Any],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_020', TestAction(
        name="3.14 is an Any",
        action=isinstance_of_typehint, args=[3.14, Any],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_021', TestAction(
        name="None is an Any",
        action=isinstance_of_typehint, args=[None, Any],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_022', TestAction(
        name="1 is an object",
        action=isinstance_of_typehint, args=[1, object],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_023', TestAction(
        name="'string' is an object",
        action=isinstance_of_typehint, args=["string", object],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_024', TestAction(
        name="b'bytes' is an object",
        action=isinstance_of_typehint, args=[b'bytes', object],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_025', TestAction(
        name="True is an object",
        action=isinstance_of_typehint, args=[True, object],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_026', TestAction(
        name="3.14 is an object",
        action=isinstance_of_typehint, args=[3.14, object],
        assertion=Assert.TRUE)),
    idspec('PRIMITIVES_027', TestAction(
        name="None is an object",
        action=isinstance_of_typehint, args=[None, object],
        assertion=Assert.TRUE)),
])
def test_primitives(typespec: TestSpec) -> None:
    """Test primitives."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('LITERALS_001', TestAction(
        name="1 is Literal[1]",
        action=isinstance_of_typehint, args=[1, Literal[1]],
        assertion=Assert.TRUE)),
    idspec('LITERALS_002', TestAction(
        name="'hello' is Literal['hello']",
        action=isinstance_of_typehint, args=["hello", Literal['hello']],
        assertion=Assert.TRUE)),
    idspec('LITERALS_003', TestAction(
        name="b'bytes' is Literal[b'bytes']",
        action=isinstance_of_typehint, args=[b'bytes', Literal[b'bytes']],
        assertion=Assert.TRUE)),
    idspec('LITERALS_004', TestAction(
        name="True is Literal[True]",
        action=isinstance_of_typehint, args=[True, Literal[True]],
        assertion=Assert.TRUE)),
    idspec('LITERALS_005', TestAction(
        name="3.14 is Literal[3.14]",
        action=isinstance_of_typehint, args=[3.14, Literal[3.14]],
        assertion=Assert.TRUE)),
    idspec('LITERALS_006', TestAction(
        name="1 is not Literal[2]",
        action=isinstance_of_typehint, args=[1, Literal[2]],
        assertion=Assert.FALSE)),
    idspec('LITERALS_007', TestAction(
        name="'hello' is not Literal['world']",
        action=isinstance_of_typehint, args=["hello", Literal['world']],
        assertion=Assert.FALSE)),
])
def test_literals(typespec: TestSpec) -> None:
    """Test literals."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('UNIONS_001', TestAction(
        name="1 is a int | str",
        action=isinstance_of_typehint, args=[1, int | str],
        assertion=Assert.TRUE)),
    idspec('UNIONS_002', TestAction(
        name="'test' is a int | str",
        action=isinstance_of_typehint, args=["test", int | str],
        assertion=Assert.TRUE)),
    idspec('UNIONS_003', TestAction(
        name="2.71 is a float | bytes",
        action=isinstance_of_typehint, args=[2.71, float | bytes],
        assertion=Assert.TRUE)),
    idspec('UNIONS_004', TestAction(
        name="b'data' is a float | bytes",
        action=isinstance_of_typehint, args=[b'data', float | bytes],
        assertion=Assert.TRUE)),
    idspec('UNIONS_005', TestAction(
        name="False is a bool | None",
        action=isinstance_of_typehint, args=[False, bool | None],
        assertion=Assert.TRUE)),
    idspec('UNIONS_006', TestAction(
        name="None is a bool | None",
        action=isinstance_of_typehint, args=[None, bool | None],
        assertion=Assert.TRUE)),
    idspec('UNIONS_007', TestAction(
        name="3+4j is a complex | int",
        action=isinstance_of_typehint, args=[3+4j, complex | int],
        assertion=Assert.TRUE)),
])
def test_unions(typespec: TestSpec) -> None:
    """Test unions."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('ANNOTATED_001', TestAction(
        name="1 is Annotated[int, 'metadata']",
        action=isinstance_of_typehint, args=[1, Annotated[int, 'metadata']],
        assertion=Assert.TRUE)),
    idspec('ANNOTATED_002', TestAction(
        name="'a' is not Annotated[int, 'metadata']",
        action=isinstance_of_typehint, args=['a', Annotated[int, 'metadata']],
        assertion=Assert.FALSE)),
    idspec('ANNOTATED_003', TestAction(
        name="'a' is Annotated[str | int, 'metadata']",
        action=isinstance_of_typehint, args=['a', Annotated[str | int, 'metadata']],
        assertion=Assert.TRUE)),
    idspec('ANNOTATED_004', TestAction(
        name="1 is Annotated[str | int, 'metadata']",
        action=isinstance_of_typehint, args=[1, Annotated[str | int, 'metadata']],
        assertion=Assert.TRUE)),
    idspec('ANNOTATED_005', TestAction(
        name="None is Annotated[None, 'metadata']",
        action=isinstance_of_typehint, args=[None, Annotated[None, 'metadata']],
        assertion=Assert.TRUE)),
])
def test_annotated(typespec: TestSpec) -> None:
    """Test annotated types."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('SETS_001', TestAction(
        name="{1, 2} is a set",
        action=isinstance_of_typehint, args=[{1, 2}, set],
        assertion=Assert.TRUE)),
    idspec('SETS_002', TestAction(
        name="{1, 2} is a set[int]",
        action=isinstance_of_typehint, args=[{1, 2}, set[int]],
        assertion=Assert.TRUE)),
    idspec('SETS_003', TestAction(
        name="{1, 'a'} is a set[int | str]",
        action=isinstance_of_typehint, args=[{1, 'a'}, set[int | str]],
        assertion=Assert.TRUE)),
    idspec('SETS_004', TestAction(
        name="{1, 2} is not a set[str]",
        action=isinstance_of_typehint, args=[{1, 2}, set[str]],
        assertion=Assert.FALSE)),
    idspec('SETS_005', TestAction(
        name="empty set is a set[int]",
        action=isinstance_of_typehint, args=[set(), set[int]],
        assertion=Assert.TRUE)),
    idspec('SETS_006', TestAction(
        name="{1, 2} is a collections.abc.Set",
        action=isinstance_of_typehint, args=[{1, 2}, Set],
        assertion=Assert.TRUE)),
    idspec('SETS_007', TestAction(
        name="{1, 2} is a collections.abc.Set[int]",
        action=isinstance_of_typehint, args=[{1, 2}, Set[int]],
        assertion=Assert.TRUE)),
    idspec('SETS_008', TestAction(
        name="frozenset({1, 2}) is a frozenset[int]",
        action=isinstance_of_typehint, args=[frozenset({1, 2}), frozenset[int]],
        assertion=Assert.TRUE)),
    idspec('SETS_009', TestAction(
        name="frozenset({1, 2}) is not a set[int]",
        action=isinstance_of_typehint, args=[frozenset({1, 2}), set[int]],
        assertion=Assert.FALSE)),
    idspec('SETS_010', TestAction(
        name="frozenset({1, 2}) is a collections.abc.Set[int]",
        action=isinstance_of_typehint, args=[frozenset({1, 2}), Set[int]],
        assertion=Assert.TRUE)),
    idspec('SETS_011', TestAction(
        name="[1, 2] is not a set[int]",
        action=isinstance_of_typehint, args=[[1, 2], set[int]],
        assertion=Assert.FALSE)),
])
def test_sets(typespec: TestSpec) -> None:
    """Test set types."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('MAPPINGS_001', TestAction(
        name="{'a': 1} is a dict",
        action=isinstance_of_typehint, args=[{'a': 1}, dict],
        assertion=Assert.TRUE)),
    idspec('MAPPINGS_002', TestAction(
        name="{'a': 1} is a dict[str, int]",
        action=isinstance_of_typehint, args=[{'a': 1}, dict[str, int]],
        assertion=Assert.TRUE)),
    idspec('MAPPINGS_003', TestAction(
        name="{'a': 1, 'b': 'c'} is a dict[str, int | str]",
        action=isinstance_of_typehint, args=[{'a': 1, 'b': 'c'}, dict[str, int | str]],
        assertion=Assert.TRUE)),
    idspec('MAPPINGS_004', TestAction(
        name="{'a': 1} is not a dict[str, str]",
        action=isinstance_of_typehint, args=[{'a': 1}, dict[str, str]],
        assertion=Assert.FALSE)),
    idspec('MAPPINGS_005', TestAction(
        name="{'a': 1} is not a dict[int, int]",
        action=isinstance_of_typehint, args=[{'a': 1}, dict[int, int]],
        assertion=Assert.FALSE)),
    idspec('MAPPINGS_006', TestAction(
        name="empty dict is a dict[str, int]",
        action=isinstance_of_typehint, args=[{}, dict[str, int]],
        assertion=Assert.TRUE)),
    idspec('MAPPINGS_007', TestAction(
        name="{'a': 1} is a Mapping",
        action=isinstance_of_typehint, args=[{'a': 1}, Mapping],
        assertion=Assert.TRUE)),
    idspec('MAPPINGS_008', TestAction(
        name="{'a': 1} is a Mapping[str, int]",
        action=isinstance_of_typehint, args=[{'a': 1}, Mapping[str, int]],
        assertion=Assert.TRUE)),
    idspec('MAPPINGS_009', TestAction(
        name="MappingProxyType is a Mapping[str, int]",
        action=isinstance_of_typehint, args=[MappingProxyType({'a': 1}), Mapping[str, int]],
        assertion=Assert.TRUE)),
    idspec('MAPPINGS_010', TestAction(
        name="{'a': {'b': 1}} is a dict[str, dict[str, int]]",
        action=isinstance_of_typehint, args=[{'a': {'b': 1}}, dict[str, dict[str, int]]],
        assertion=Assert.TRUE)),
    idspec('MAPPINGS_011', TestAction(
        name="{'a': {'b': 1}} is not a dict[str, dict[str, str]]",
        action=isinstance_of_typehint, args=[{'a': {'b': 1}}, dict[str, dict[str, str]]],
        assertion=Assert.FALSE)),
    idspec('MAPPINGS_012', TestAction(
        name="[1, 2] is not a dict",
        action=isinstance_of_typehint, args=[[1, 2], dict],
        assertion=Assert.FALSE)),
])
def test_mappings(typespec: TestSpec) -> None:
    """Test mapping types."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('SEQUENCES_001', TestAction(
        name="[1, 2] is a list",
        action=isinstance_of_typehint, args=[[1, 2], list],
        assertion=Assert.TRUE)),
    idspec('SEQUENCES_002', TestAction(
        name="[1, 2] is a list[int]",
        action=isinstance_of_typehint, args=[[1, 2], list[int]],
        assertion=Assert.TRUE)),
    idspec('SEQUENCES_003', TestAction(
        name="[1, 'a'] is a list[int | str]",
        action=isinstance_of_typehint, args=[[1, 'a'], list[int | str]],
        assertion=Assert.TRUE)),
    idspec('SEQUENCES_004', TestAction(
        name="[1, 2] is not a list[str]",
        action=isinstance_of_typehint, args=[[1, 2], list[str]],
        assertion=Assert.FALSE)),
    idspec('SEQUENCES_005', TestAction(
        name="empty list is a list[int]",
        action=isinstance_of_typehint, args=[[], list[int]],
        assertion=Assert.TRUE)),
    idspec('SEQUENCES_006', TestAction(
        name="[1, 2] is a collections.abc.Sequence",
        action=isinstance_of_typehint, args=[[1, 2], Sequence],
        assertion=Assert.TRUE)),
    idspec('SEQUENCES_007', TestAction(
        name="[1, 2] is a collections.abc.Sequence[int]",
        action=isinstance_of_typehint, args=[[1, 2], Sequence[int]],
        assertion=Assert.TRUE)),
    idspec('SEQUENCES_008', TestAction(
        name="(1, 2) is a tuple[int, int]",
        action=isinstance_of_typehint, args=[(1, 2), tuple[int, int]],
        assertion=Assert.TRUE)),
    idspec('SEQUENCES_009', TestAction(
        name="(1, 2) is a collections.abc.Sequence[int]",
        action=isinstance_of_typehint, args=[(1, 2), Sequence[int]],
        assertion=Assert.TRUE)),
    idspec('SEQUENCES_010', TestAction(
        name="[[1], [2]] is a list[list[int]]",
        action=isinstance_of_typehint, args=[[[1], [2]], list[list[int]]],
        assertion=Assert.TRUE)),
    idspec('SEQUENCES_011', TestAction(
        name="[[1], [2]] is not a list[list[str]]",
        action=isinstance_of_typehint, args=[[[1], [2]], list[list[str]]],
        assertion=Assert.FALSE)),
    idspec('SEQUENCES_012', TestAction(
        name="{'a': 1} is not a list",
        action=isinstance_of_typehint, args=[{'a': 1}, list],
        assertion=Assert.FALSE)),
])
def test_sequences(typespec: TestSpec) -> None:
    """Test sequence types."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('ITERABLES_001', TestAction(
        name="[1, 2] is an Iterable",
        action=isinstance_of_typehint, args=[[1, 2], Iterable],
        assertion=Assert.TRUE)),
    idspec('ITERABLES_002', TestAction(
        name="[1, 2] is an Iterable[int]",
        action=isinstance_of_typehint, args=[[1, 2], Iterable[int]],
        assertion=Assert.TRUE)),
    idspec('ITERABLES_003', TestAction(
        name="{1, 2} is an Iterable[int]",
        action=isinstance_of_typehint, args=[{1, 2}, Iterable[int]],
        assertion=Assert.TRUE)),
    idspec('ITERABLES_004', TestAction(
        name="(1, 2) is an Iterable[int]",
        action=isinstance_of_typehint, args=[(1, 2), Iterable[int]],
        assertion=Assert.TRUE)),
    idspec('ITERABLES_005', TestAction(
        name="'abc' is an Iterable[str]",
        action=isinstance_of_typehint, args=['abc', Iterable[str]],
        assertion=Assert.TRUE)),
    idspec('ITERABLES_006', TestAction(
        name="b'abc' is an Iterable[int]",
        action=isinstance_of_typehint, args=[b'abc', Iterable[int]],
        assertion=Assert.TRUE)),
    idspec('ITERABLES_007', TestAction(
        name="{'a': 1} is an Iterable[str] (keys)",
        action=isinstance_of_typehint, args=[{'a': 1}, Iterable[str]],
        assertion=Assert.TRUE)),
    idspec('ITERABLES_008', TestAction(
        name="[1, 2] is not an Iterable[str]",
        action=isinstance_of_typehint, args=[[1, 2], Iterable[str]],
        assertion=Assert.FALSE)),
    idspec('ITERABLES_009', TestAction(
        name="empty list is an Iterable[int]",
        action=isinstance_of_typehint, args=[[], Iterable[int]],
        assertion=Assert.TRUE)),
    idspec('ITERABLES_010', TestAction(
        name="123 is not an Iterable",
        action=isinstance_of_typehint, args=[123, Iterable],
        assertion=Assert.FALSE)),
    idspec('ITERABLES_011', TestAction(
        name="generator is an Iterable[int]",
        action=isinstance_of_typehint, args=[(i for i in range(3)), Iterable[int]],
        kwargs={'consume_iterators': True},
        assertion=Assert.TRUE)),
    idspec('ITERABLES_012', TestAction(
        name="generator is not an Iterable[str]",
        action=isinstance_of_typehint, args=[(i for i in range(3)), Iterable[str]],
        kwargs={'consume_iterators': True},
        assertion=Assert.FALSE)),
])
def test_iterables(typespec: TestSpec) -> None:
    """Test iterable types."""
    clear_typehint_cache()
    typespec.run()


def typeddict_testspec() -> list[TestSpec]:
    """Generate TypedDict test specifications."""

    class TDImplicitRequiredDict(TypedDict):
        """TypedDict with implicitly required fields."""
        a: int
        b: str

    testspecs: list[TestSpec] = [
        idspec('TYPEDDICT_001', TestAction(
            name="{'a': 1, 'b': 'x'} is a TypedDict with correct types and required fields",
            action=isinstance_of_typehint, args=[{'a': 1, 'b': 'x'}, TDImplicitRequiredDict],
            assertion=Assert.TRUE)),
        idspec('TYPEDDICT_002', TestAction(
            name="{'a': 1, 'b': 1} is a TypedDict with wrong type for 'b' and required fields",
            action=isinstance_of_typehint, args=[{'a': 1, 'b': 1}, TDImplicitRequiredDict],
            assertion=Assert.FALSE)),
        idspec('TYPEDDICT_003', TestAction(
            name="{'a': 't', 'b': 'x'} is a TypedDict with wrong type for 'a' and required fields",
            action=isinstance_of_typehint, args=[{'a': 't', 'b': 'x'}, TDImplicitRequiredDict],
            assertion=Assert.FALSE)),
        idspec('TYPEDDICT_004', TestAction(
            name="{'a': 1} is a TypedDict missing required field 'b'",
            action=isinstance_of_typehint, args=[{'a': 1}, TDImplicitRequiredDict],
            assertion=Assert.FALSE)),
        idspec('TYPEDDICT_005', TestAction(
            name="{'b': 'x'} is a TypedDict missing required field 'a'",
            action=isinstance_of_typehint, args=[{'b': 'x'}, TDImplicitRequiredDict],
            assertion=Assert.FALSE)),
        idspec('TYPEDDICT_006', TestAction(
            name="{'a': 1, 'b': 'x', 'c': 3.14} is a TypedDict with invalid extra field 'c'",
            action=isinstance_of_typehint, args=[{'a': 1, 'b': 'x', 'c': 3.14}, TDImplicitRequiredDict],
            assertion=Assert.FALSE)),
        idspec('TYPEDDICT_007', TestAction(
            name="{} is a TypedDict with all required fields missing",
            action=isinstance_of_typehint,
            args=[{}, TDImplicitRequiredDict],
            assertion=Assert.FALSE)),
    ]

    class TDNotRequiredDict(TypedDict, total=False):
        """TypedDict with no required fields."""
        a: int
        b: str

    testspecs.extend([
        idspec('TYPEDDICT_008', TestAction(
            name="{'a': 1, 'b': 'x'} is a TypedDict with correct types and no required fields",
            action=isinstance_of_typehint, args=[{'a': 1, 'b': 'x'}, TDNotRequiredDict],
            assertion=Assert.TRUE)),
        idspec('TYPEDDICT_009', TestAction(
            name="{'a': 1} is a TypedDict with missing field 'b' and no required fields",
            action=isinstance_of_typehint, args=[{'a': 1}, TDNotRequiredDict],
            assertion=Assert.TRUE)),
        idspec('TYPEDDICT_010', TestAction(
            name="{} is a TypedDict with all fields missing and no required fields",
            action=isinstance_of_typehint,
            args=[{}, TDNotRequiredDict],
            assertion=Assert.TRUE)),
        idspec('TYPEDDICT_011', TestAction(
            name="{'a': 't', 'b': 'x'} is a TypedDict with wrong type for 'a' and no required fields",
            action=isinstance_of_typehint, args=[{'a': 't', 'b': 'x'}, TDNotRequiredDict],
            assertion=Assert.FALSE)),
        idspec('TYPEDDICT_012', TestAction(
            name="{'a': 1, 'b': 'x', 'c': 3.14} is a TypedDict with invalid extra field 'c' and no required fields",
            action=isinstance_of_typehint, args=[{'a': 1, 'b': 'x', 'c': 3.14}, TDNotRequiredDict],
            assertion=Assert.FALSE)),
    ])

    class TDMixedRequiredFieldsDict(TypedDict, total=True):
        """TypedDict with mixed required and not required fields (total=True).
        a - required
        c - required
        """
        a: int
        c: Required[float]

    class TDMixedDict(TDMixedRequiredFieldsDict, total=False):
        """TypedDict with mixed required and not required fields.
        a - required
        b - not required
        c - required
        """
        b: NotRequired[str]

    testspecs.extend([
        idspec('TYPEDDICT_013', TestAction(
            name="{'a': 1, 'c': 3.14} is a TypedDict with required fields and missing not required field",
            action=isinstance_of_typehint, args=[{'a': 1, 'c': 3.14}, TDMixedDict],
            assertion=Assert.TRUE)),
        idspec('TYPEDDICT_014', TestAction(
            name="{'a': 1, 'b': 'x', 'c': 3.14} is a TypedDict with all fields present",
            action=isinstance_of_typehint, args=[{'a': 1, 'b': 'x', 'c': 3.14}, TDMixedDict],
            assertion=Assert.TRUE)),
        idspec('TYPEDDICT_015', TestAction(
            name="{'a': 1} is a TypedDict missing required field 'c'",
            action=isinstance_of_typehint, args=[{'a': 1}, TDMixedDict],
            assertion=Assert.FALSE)),
        idspec('TYPEDDICT_016', TestAction(
            name="{'c': 3.14} is a TypedDict missing required field 'a'",
            action=isinstance_of_typehint, args=[{'c': 3.14}, TDMixedDict],
            assertion=Assert.FALSE)),
        idspec('TYPEDDICT_017', TestAction(
            name="{'a': 't', 'c': 3.14} is a TypedDict with wrong type for 'a'",
            action=isinstance_of_typehint, args=[{'a': 't', 'c': 3.14}, TDMixedDict],
            assertion=Assert.FALSE)),
        idspec('TYPEDDICT_018', TestAction(
            name="{'a': 1, 'c': 'pi'} is a TypedDict with wrong type for 'c'",
            action=isinstance_of_typehint, args=[{'a': 1, 'c': 'pi'}, TDMixedDict],
            assertion=Assert.FALSE)),
    ])

    return testspecs

@pytest.mark.parametrize('typespec', typeddict_testspec())
def test_typeddict(typespec: TestSpec) -> None:
    """Test TypedDict types."""
    clear_typehint_cache()
    typespec.run()


@pytest.mark.parametrize('typespec', [
    idspec('COLLECTION_001', TestAction(
        name='[1, 2, 3] is a Collection',
        action=isinstance_of_typehint, args=[[1, 2, 3], Collection],
        assertion=Assert.TRUE)),
    idspec('COLLECTION_002', TestAction(
        name='[1, 2, 3] is a Collection[int]',
        action=isinstance_of_typehint, args=[[1, 2, 3], Collection[int]],
        assertion=Assert.TRUE)),
    idspec('COLLECTION_003', TestAction(
        name='(1, 2, 3) is a Collection[int]',
        action=isinstance_of_typehint, args=[(1, 2, 3), Collection[int]],
        assertion=Assert.TRUE)),
    idspec('COLLECTION_004', TestAction(
        name='{1, 2, 3} is a Collection[int]',
        action=isinstance_of_typehint, args=[{1, 2, 3}, Collection[int]],
        assertion=Assert.TRUE)),
    idspec('COLLECTION_005', TestAction(
        name='frozenset({1, 2, 3}) is a Collection[int]',
        action=isinstance_of_typehint, args=[frozenset({1, 2, 3}), Collection[int]],
        assertion=Assert.TRUE)),
    idspec('COLLECTION_006', TestAction(
        name='[1, "a", 3] is not a Collection[int]',
        action=isinstance_of_typehint, args=[[1, "a", 3], Collection[int]],
        assertion=Assert.FALSE)),
    idspec('COLLECTION_007', TestAction(
        name='123 is not a Collection',
        action=isinstance_of_typehint, args=[123, Collection],
        assertion=Assert.FALSE)),
    idspec('COLLECTION_008', TestAction(
        name='empty list is a Collection[int]',
        action=isinstance_of_typehint, args=[[], Collection[int]],
        assertion=Assert.TRUE)),
])
def test_collections(typespec: TestSpec) -> None:
    """Test Collection types."""
    clear_typehint_cache()
    typespec.run()


def newtype_testspec() -> list[TestSpec]:
    """Generate NewType test specifications."""
    NewInt = NewType('NewInt', int)

    testspecs = [
        idspec('NEWTYPE_001', TestAction(
            name="NewInt(5) is a NewType of int",
            action=isinstance_of_typehint, args=[NewInt(5), NewInt],
            assertion=Assert.TRUE)),
        idspec('NEWTYPE_002', TestAction(
            name="NewInt(5) is an int",
            action=isinstance_of_typehint, args=[NewInt(5), int],
            assertion=Assert.TRUE)),
            # Wierd true fact! NewType types are a 'noop' at runtime:
            # It returns the original object unchanged. The most we can do is check
            # is that the value is compatible with the underlying type.
        idspec('NEWTYPE_003', TestAction(
            name="5 is compatible with a NewType of int",
            action=isinstance_of_typehint, args=[5, NewInt],
            assertion=Assert.TRUE)),
        idspec('NEWTYPE_004', TestAction(
            name="'hello' is not compatible with a NewType of int",
            action=isinstance_of_typehint, args=['hello', NewInt],
            assertion=Assert.FALSE)),
    ]
    return testspecs

@pytest.mark.parametrize('testspec', newtype_testspec())
def test_newtype(testspec: TestSpec) -> None:
    """Test NewType."""
    clear_typehint_cache()
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec('FINAL_001', TestAction(
        name="Final[int] accepts int",
        action=isinstance_of_typehint,
        args=[10, Final[int]],
        assertion=Assert.TRUE)),
    idspec('FINAL_002', TestAction(
        name="Final[str] accepts str",
        action=isinstance_of_typehint,
        args=["test", Final[str]],
        assertion=Assert.TRUE)),
    idspec('FINAL_003', TestAction(
        name="Final[str] rejects int",
        action=isinstance_of_typehint, args=[10, Final[str]],
        assertion=Assert.FALSE)),
    idspec('FINAL_004', TestAction(
        name="Final[int] rejects str",
        action=isinstance_of_typehint, args=["test", Final[int]],
        assertion=Assert.FALSE)),
])
def test_final_typehint(testspec: TestSpec) -> None:
    """Test Final typehint."""
    clear_typehint_cache()
    testspec.run()

def userclass_testspecs() -> list:
    """Test that user-defined class instances are correctly identified."""

    class MyClass:
        pass

    instance = MyClass()

    testspecs: list[TestSpec] = [
        idspec('USERCLASS_001', TestAction(
            name="MyClass instance is a MyClass",
            action=isinstance_of_typehint, args=[instance, MyClass],
            assertion=Assert.TRUE)),
        idspec('USERCLASS_002', TestAction(
            name="MyClass instance is an object",
            action=isinstance_of_typehint, args=[instance, object],
            assertion=Assert.TRUE)),
        idspec('USERCLASS_003', TestAction(
            name="MyClass instance is not an int",
            action=isinstance_of_typehint, args=[instance, int],
            assertion=Assert.FALSE)),
    ]
    return testspecs

@pytest.mark.parametrize('testspec', userclass_testspecs())
def test_userclass_instance(testspec: TestSpec) -> None:
    testspec.run()


def nested_types_testspecs() -> list[TestSpec]:
    """Test nested type hints like list[dict[str, int]]."""

    testspecs: list[TestSpec] = [
        idspec('NESTED_001', TestAction(
            name="[{ 'a': 1 }, { 'b': 2 }] is a list[dict[str, int]]",
            action=isinstance_of_typehint,
            args=[[{'a': 1}, {'b': 2}], list[dict[str, int]]],
            assertion=Assert.TRUE)),
        idspec('NESTED_002', TestAction(
            name="[{ 'a': 'x' }, { 'b': 2 }] is not a list[dict[str, int]]",
            action=isinstance_of_typehint,
            args=[[{'a': 'x'}, {'b': 2}], list[dict[str, int]]],
            assertion=Assert.FALSE)),
    ]
    return testspecs

@pytest.mark.parametrize('testspec', nested_types_testspecs())
def test_nested_types(testspec: TestSpec) -> None:
    testspec.run()



def enum_testspecs() -> list[TestSpec]:
    """Test Enum type hints."""

    class Color(enum.Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    testspecs: list[TestSpec] = [
        idspec('ENUM_001', TestAction(
            name='Color.RED is a Color',
            action=isinstance_of_typehint, args=[Color.RED, Color],
            assertion=Assert.TRUE)),
        idspec('ENUM_002', TestAction(
            name='Color.GREEN is a Color',
            action=isinstance_of_typehint, args=[Color.GREEN, Color],
            assertion=Assert.TRUE)),
        idspec('ENUM_003', TestAction(
            name='1 is not a Color',
            action=isinstance_of_typehint, args=[1, Color],
            assertion=Assert.FALSE)),
        idspec('ENUM_004', TestAction(
            name="'RED' is not a Color'",
            action=isinstance_of_typehint, args=['RED', Color],
            assertion=Assert.FALSE)),
    ]
    return testspecs

@pytest.mark.parametrize('testspec', enum_testspecs())
def test_enum_typehint(testspec: TestSpec) -> None:
    """Test Enum typehint."""
    clear_typehint_cache()
    testspec.run()


def callable_testspecs() -> list[TestSpec]:
    """Test Callable type hints."""

    def func_no_args() -> int:
        return 42

    def func_one_arg(x: int) -> str:
        return str(x)

    def func_two_args(x: int, y: str) -> float:
        return float(x)

    class CallableClass:
        def __call__(self, x: int) -> str:
            return str(x)

    testspecs: list[TestSpec] = [
        idspec('CALLABLE_001', TestAction(
            name='func_no_args is a Callable',
            action=isinstance_of_typehint, args=[func_no_args, Callable],
            assertion=Assert.TRUE)),
        idspec('CALLABLE_002', TestAction(
            name='func_one_arg is a Callable[[int], str]',
            action=isinstance_of_typehint, args=[func_one_arg, Callable[[int], str]],
            assertion=Assert.TRUE)),
        idspec('CALLABLE_003', TestAction(
            name='func_two_args is a Callable[[int, str], float]',
            action=isinstance_of_typehint, args=[func_two_args, Callable[[int, str], float]],
            assertion=Assert.TRUE)),
        idspec('CALLABLE_004', TestAction(
            name='CallableClass() is a Callable[[int], str]',
            action=isinstance_of_typehint, args=[CallableClass(), Callable[[int], str]],
            assertion=Assert.TRUE)),
        idspec('CALLABLE_005', TestAction(
            name='func_no_args is not a Callable[[int], str]',
            action=isinstance_of_typehint, args=[func_no_args, Callable[[int], str]],
            assertion=Assert.FALSE)),
        idspec('CALLABLE_006', TestAction(
            name='func_one_arg is not a Callable[[str], str]',
            action=isinstance_of_typehint, args=[func_one_arg, Callable[[str], str]],
            assertion=Assert.FALSE)),
        idspec('CALLABLE_007', TestAction(
            name='42 is not a Callable',
            action=isinstance_of_typehint, args=[42, Callable],
            assertion=Assert.FALSE)),
    ]
    return testspecs

@pytest.mark.parametrize('testspec', callable_testspecs())
def test_callable_typehint(testspec: TestSpec) -> None:
    """Test Callable typehint."""
    clear_typehint_cache()
    testspec.run()

def generic_sequence_subclass_testspecs() -> list[TestSpec]:
    """Test generic subclasses of Sequence."""

    class MyIntSeq(Sequence[int]):
        def __init__(self, data):
            self._data = list(data)
        def __getitem__(self, idx):
            return self._data[idx]
        def __len__(self):
            return len(self._data)

    class MyStrSeq(Sequence[str]):
        def __init__(self, data):
            self._data = list(data)
        def __getitem__(self, idx):
            return self._data[idx]
        def __len__(self):
            return len(self._data)

    int_seq = MyIntSeq([1, 2, 3])
    str_seq = MyStrSeq(['a', 'b', 'c'])

    testspecs: list[TestSpec] = [
        idspec('GENSEQ_001', TestAction(
            name='MyIntSeq([1, 2, 3]) is a Sequence[int]',
            action=isinstance_of_typehint, args=[int_seq, Sequence[int]],
            assertion=Assert.TRUE)),
        idspec('GENSEQ_002', TestAction(
            name='MyStrSeq(["a", "b", "c"]) is a Sequence[str]',
            action=isinstance_of_typehint, args=[str_seq, Sequence[str]],
            assertion=Assert.TRUE)),
        idspec('GENSEQ_003', TestAction(
            name='MyIntSeq([1, 2, 3]) is not a Sequence[str]',
            action=isinstance_of_typehint, args=[int_seq, Sequence[str]],
            assertion=Assert.FALSE)),
        idspec('GENSEQ_004', TestAction(
            name='MyStrSeq(["a", "b", "c"]) is not a Sequence[int]',
            action=isinstance_of_typehint, args=[str_seq, Sequence[int]],
            assertion=Assert.FALSE)),
        idspec('GENSEQ_005', TestAction(
            name='MyIntSeq([1, 2, 3]) is a Sequence',
            action=isinstance_of_typehint, args=[int_seq, Sequence],
            assertion=Assert.TRUE)),
        idspec('GENSEQ_006', TestAction(
            name='MyStrSeq(["a", "b", "c"]) is a Sequence',
            action=isinstance_of_typehint, args=[str_seq, Sequence],
            assertion=Assert.TRUE)),
    ]
    return testspecs

@pytest.mark.parametrize('testspec', generic_sequence_subclass_testspecs())
def test_generic_sequence_subclass(testspec: TestSpec) -> None:
    """Test generic subclasses of Sequence."""
    clear_typehint_cache()
    testspec.run()

@pytest.mark.parametrize('testspec', [
    idspec('ANY_001', TestAction(
        name='1 is an Any',
        action=isinstance_of_typehint, args=[1, Any],
        assertion=Assert.TRUE)),
    idspec('ANY_002', TestAction(
        name="'string' is an Any",
        action=isinstance_of_typehint, args=['string', Any],
        assertion=Assert.TRUE)),
    idspec('ANY_003', TestAction(
        name='[1, 2, 3] is an Any',
        action=isinstance_of_typehint, args=[[1, 2, 3], Any],
        assertion=Assert.TRUE)),
    idspec('ANY_004', TestAction(
        name='None is an Any',
        action=isinstance_of_typehint, args=[None, Any],
        assertion=Assert.TRUE)),
    idspec('ANY_005', TestAction(
        name='object() is an Any',
        action=isinstance_of_typehint, args=[object(), Any],
        assertion=Assert.TRUE)),
])
def test_any_typehint(testspec: TestSpec) -> None:
    """Test Any typehint."""
    clear_typehint_cache()
    testspec.run()

@pytest.mark.parametrize('testspec', [
    idspec('HASHABLE_001', TestAction(
        name='1 is Hashable',
        action=isinstance_of_typehint, args=[1, Hashable],
        assertion=Assert.TRUE)),
    idspec('HASHABLE_002', TestAction(
        name="'a' is Hashable",
        action=isinstance_of_typehint, args=['a', Hashable],
        assertion=Assert.TRUE)),
    idspec('HASHABLE_003', TestAction(
        name='(1, 2) is Hashable',
        action=isinstance_of_typehint, args=[(1, 2), Hashable],
        assertion=Assert.TRUE)),
    idspec('HASHABLE_004', TestAction(
        name='[1, 2] is not Hashable',
        action=isinstance_of_typehint, args=[[1, 2], Hashable],
        assertion=Assert.FALSE)),
    idspec('HASHABLE_005', TestAction(
        name='{1: 2} is not Hashable',
        action=isinstance_of_typehint, args=[{1: 2}, Hashable],
        assertion=Assert.FALSE)),
    idspec('HASHABLE_006', TestAction(
        name='frozenset({1, 2}) is Hashable',
        action=isinstance_of_typehint, args=[frozenset({1, 2}), Hashable],
        assertion=Assert.TRUE)),
    idspec('HASHABLE_007', TestAction(
        name='set([1, 2]) is not Hashable',
        action=isinstance_of_typehint, args=[set([1, 2]), Hashable],
        assertion=Assert.FALSE)),
])
def test_hashable_typehint(testspec: TestSpec) -> None:
    """Test Hashable typehint."""
    clear_typehint_cache()
    testspec.run()

def protocols_testspecs() -> list[TestSpec]:
    """Tests for protocols."""

    class MyProtocol(Protocol):
        """non-runtime checkable Protocol for testing."""
        def foo(self) -> int: ...

    @runtime_checkable
    class MyCheckableProtocol(Protocol):
        """runtime checkable Protocol for testing."""
        def foo(self) -> int: ...

    class MyProtocolImpl:
        """Implementation of MyCheckableProtocol."""
        def foo(self) -> int:
            return 42


    testspecs: list[TestSpec] = [
        idspec('PROTOCOLS_001', TestAction(
            name='object() is not instance of a non-runtime checkable Protocol',
            action=isinstance_of_typehint, args=[object(), MyProtocol],
            assertion=Assert.FALSE)),
        idspec('PROTOCOLS_002', TestAction(
            name='object() is not instance of a runtime checkable Protocol',
            action=isinstance_of_typehint, args=[object(), MyCheckableProtocol],
            assertion=Assert.FALSE)),
        idspec('PROTOCOLS_003', TestAction(
            name='MyProtocolImpl() is instance of a runtime checkable Protocol',
            action=isinstance_of_typehint, args=[MyProtocolImpl(), MyCheckableProtocol],
            assertion=Assert.TRUE)),
    ]
    return testspecs

@pytest.mark.parametrize('testspec', protocols_testspecs())
def test_protocols(testspec: TestSpec) -> None:
    """Tests for protocols."""
    clear_typehint_cache()
    testspec.run()

if __name__ == '__main__':
    pytest.main([__file__, "--log-cli-level=DEBUG", '-s'])
