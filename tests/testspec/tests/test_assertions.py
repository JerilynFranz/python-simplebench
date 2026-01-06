import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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

from testspec import Assert, TestSpec, idspec
from testspec.assertions import validate_assertion


@dataclass
class AssertTest(TestSpec):
    """Test case for assertion validation."""
    name: str
    assertion: Assert
    expected: Any
    found: Any
    should_pass: bool

    def run(self) -> None:
        """Dummy run method for AssertTest."""
        pass


@pytest.mark.parametrize("test_case", [
    idspec('ASSERT_001', AssertTest('EQUAL 5 == 5, True', Assert.EQUAL, 5, 5, True)),
    idspec('ASSERT_002', AssertTest('NOT_EQUAL, 5 != 3, True', Assert.NOT_EQUAL, 5, 3, True)),
    idspec('ASSERT_003', AssertTest('LESS_THAN 3 < 5, True', Assert.LESS_THAN, 5, 3, True)),
    idspec('ASSERT_004', AssertTest('LESS_THAN_OR_EQUAL 5 <= 5, True', Assert.LESS_THAN_OR_EQUAL, 5, 5, True)),
    idspec('ASSERT_005', AssertTest('GREATER_THAN 10 > 5, True', Assert.GREATER_THAN, 5, 10, True)),
    idspec('ASSERT_006', AssertTest('GREATER_THAN_OR_EQUAL 10 >= 6, True', Assert.GREATER_THAN_OR_EQUAL, 6, 10, True)),
    idspec('ASSERT_007', AssertTest('IN a in apple, True', Assert.IN, 'a', 'apple', True)),
    idspec('ASSERT_008', AssertTest('NOT_IN z not in apple, True', Assert.NOT_IN, 'z', 'apple', True)),
    idspec('ASSERT_009', AssertTest('IS None is None, True', Assert.IS, None, None, True)),
    idspec('ASSERT_010', AssertTest('IS_NOT None is not 5, True', Assert.IS_NOT, None, 5, True)),
    idspec('ASSERT_011', AssertTest('ISINSTANCE 5 is instance of int, True', Assert.ISINSTANCE, int, 5, True)),
    idspec('ASSERT_012', AssertTest('ISSUBCLASS ValueError is subclass of Exception, True', Assert.ISSUBCLASS, Exception, ValueError, True)),
    idspec('ASSERT_013', AssertTest('IS_NONE None is None, True', Assert.IS_NONE, None, None, True)),
    idspec('ASSERT_014', AssertTest('IS_NOT_NONE None is not 5, True', Assert.IS_NOT_NONE, None, 5, True)),
    idspec('ASSERT_015', AssertTest('TRUE, True', Assert.TRUE, None, True, True)),
    idspec('ASSERT_016', AssertTest('FALSE, False', Assert.FALSE, None, False, True)),
    idspec('ASSERT_017', AssertTest('LEN len([1, 2, 3]) == 3, True', Assert.LEN, 3, [1, 2, 3], True)),
    # Failing cases
    idspec('ASSERT_018', AssertTest('EQUAL 5 == 3, False', Assert.EQUAL, 5, 3, False)),
    idspec('ASSERT_019', AssertTest('NOT_EQUAL 5 != 5, False', Assert.NOT_EQUAL, 5, 5, False)),
    idspec('ASSERT_020', AssertTest('LESS_THAN 5 < 3, False', Assert.LESS_THAN, 3, 5, False)),
    idspec('ASSERT_021', AssertTest('LESS_THAN_OR_EQUAL 5 <= 3, False', Assert.LESS_THAN_OR_EQUAL, 3, 5, False)),
    idspec('ASSERT_022', AssertTest('GREATER_THAN 3 > 5, False', Assert.GREATER_THAN, 5, 3, False)),
    idspec('ASSERT_023', AssertTest('GREATER_THAN_OR_EQUAL 3 >= 5, False', Assert.GREATER_THAN_OR_EQUAL, 5, 3, False)),
    idspec('ASSERT_024', AssertTest('IN z in apple, False', Assert.IN, 'z', 'apple', False)),
    idspec('ASSERT_025', AssertTest('NOT_IN a not in apple, False', Assert.NOT_IN, 'a', 'apple', False)),
    idspec('ASSERT_026', AssertTest('IS None is 5, False', Assert.IS, None, 5, False)),
    idspec('ASSERT_027', AssertTest('IS_NOT None is not None, False', Assert.IS_NOT, None, None, False)),
    idspec('ASSERT_028', AssertTest('ISINSTANCE 5 is instance of str, False', Assert.ISINSTANCE, int, '5', False)),
    idspec('ASSERT_029', AssertTest('ISSUBCLASS Exception is subclass of int, False', Assert.ISSUBCLASS, Exception, int, False)),
    idspec('ASSERT_030', AssertTest('IS_NONE None is None, False', Assert.IS_NONE, None, 5, False)),
    idspec('ASSERT_031', AssertTest('IS_NOT_NONE None is not None, False', Assert.IS_NOT_NONE, None, None, False)),
    idspec('ASSERT_032', AssertTest('TRUE True, False', Assert.TRUE, None, False, False)),
    idspec('ASSERT_033', AssertTest('FALSE False, False', Assert.FALSE, None, True, False)),
    idspec('ASSERT_034', AssertTest('LEN len([1, 2, 3]) == 2, False', Assert.LEN, 2, [1, 2, 3], False)),
])
def test_assertions(test_case: AssertTest):
    """Test the assertion validation logic."""
    error_message = validate_assertion(test_case.assertion, test_case.expected, test_case.found)
    if test_case.should_pass:
        assert error_message == "", f"{test_case.name}: {error_message}"
    else:
        assert error_message != "", f"{test_case.name}: Expected assertion to fail but it passed"


if __name__ == "__main__":
    pytest.main([__file__, '-s'])
