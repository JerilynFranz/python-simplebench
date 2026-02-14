"""Factories for report.v1.python_info."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.kwargs.report.v1 import PythonInfoKWArgs


@cache
def python_info_kwargs() -> PythonInfoKWArgs:
    """PythonInfoKwargs factory for testing purposes.

    :return: A PythonInfoKwargs instance with dummy data.
    :rtype: PythonInfoWArgs
    """
    data = python_info_data()
    return PythonInfoKWArgs(
        hash_id=data['hash_id'],  # type: ignore[call-arg]
        python_version=data['python_version'],
        implementation=data['implementation'],
        implementation_version=data['implementation_version'],
        compiler=data['compiler'],
        revision=data['revision'],
        buildno=data['buildno'],
        builddate=data['builddate'],
        command_line_flags=data['command_line_flags'],
        environment_variables=data['environment_variables'],
        gc_is_enabled=data['gc_is_enabled'],
        gc_thresholds=data['gc_thresholds'],
        thread_switch_interval=data['thread_switch_interval'],
        architecture_bits=data['architecture_bits'],
        architecture_linkage=data['architecture_linkage'],
    )


@cache
def python_info() -> report.PythonInfo:
    """PythonInfo factory for testing purposes.

    :return: A PythonInfo instance with dummy data.
    :rtype: report.PythonInfo
    """
    return report.PythonInfo(**python_info_kwargs())

"""Factories for creating report PythonInfoData instances with dummy data for testing."""

def python_info_data() -> report.PythonInfoData:
    """PythonInfoData factory for testing purposes.

    :return: A PythonInfoData instance with dummy data.
    :rtype: report.PythonInfoData
    """
    info = report.PythonInfoData(
        hash_id='c' * 64,
        type=report.PythonInfoSchema.TYPE,
        version=report.PythonInfoSchema.VERSION,
        python_version='3.12.3',
        implementation='CPython',
        implementation_version='3.12.3',
        compiler='Clang 13.0.0 (clang-1300.0.29.30)',
        revision='f6650f9ad7',
        buildno='v3.12.3:f6650f9ad7',
        builddate='Apr  9 2024 08:18:47',
        command_line_flags='-R -X int_max_str_digits',
        environment_variables={
            'PYTHONPATH': 'src:tests',
            'PYTHON_BASIC_REPL': '1'},
        gc_is_enabled=True,
        gc_thresholds=(700, 10, 10),
        thread_switch_interval=0.005,
        architecture_bits='64bit',
        architecture_linkage='')
    if 'hash_id' not in info:  # type: ignore[typeddict-item]
        raise TypeError(f'Generated info is missing required hash_id field: {info!r}')
    if not is_typed_dict_mimic(info, report.PythonInfoData):
        raise TypeError(f'Generated info does not conform to PythonInfoData TypedDict: {info!r}')
    return info

def no_hash_id_python_info_data() -> report.PythonInfoData:
    """PythonInfoData factory for testing purposes.

    :return: A PythonInfoData instance with dummy data.
    :rtype: report.PythonInfoData
    """
    info = python_info_data()
    del info['hash_id']  # type: ignore[typeddict-item]
    if not is_typed_dict_mimic(info, report.PythonInfoData):
        raise TypeError(f'Generated info does not conform to PythonInfoData TypedDict: {info!r}')
    return info


