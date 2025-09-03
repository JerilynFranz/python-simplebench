#!/usr/bin/env python3
"""Pytest launcher for simplebench tests.

Usage:
  ./test_plan.py                # run all tests under tests/gentrie

Environment (optional):
  SIMPLEBENCH_FAIL_FAST=1           # enable fail-fast (-x)
"""

from __future__ import annotations

import os
import sys
import pytest


def build_pytest_args() -> list[str]:
    args: list[str] = []
    # Fail fast
    if os.environ.get("SIMPLEBENCH_FAIL_FAST") == "1":
        args.append("-x")
    # Quiet by default; adjust as needed
    args.extend(["-q", "--disable-warnings"])
    # Add test path
    args.append("tests/gentrie")

    return args


def main() -> int:
    args = build_pytest_args()
    return pytest.main(args)  #


if __name__ == "__main__":
    sys.exit(main())
