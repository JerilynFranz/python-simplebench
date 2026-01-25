"""Validators for reporter-related entities."""
from argparse import Namespace
from collections.abc import Set
from pathlib import Path
from typing import TYPE_CHECKING, Any

from requests import Session

from simplebench.enums import Format, Target
from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metadata import Metadata
from simplebench.metrics import Metric, MetricsCollection
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter.config import ReporterConfig
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.simplebench_types import is_element_collection
from simplebench.type_proxies import is_case, is_choice, is_session

from ._error_tags import _ReporterErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice
    from simplebench.session.session import Session
    from simplebench.reporters.reporter.reporter import Reporter

# No need to export any names from this module directly
__all__ = []


def cls_type(value: Any, field_name: str = 'cls_type') -> type:
    """Validate that the provided value is a type.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'cls_type') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a type.

    :return: The validated type.
    """
    if not isinstance(value, type):
        message = f'Expected a type for {field_name!r}: got {type(value).__name__}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_CLS_ARG_TYPE
            )
    return value

def reporter_options(value: Any, field_name: str = 'reporter_options') -> tuple[ReporterOptions, ...]:
    """Validate that the provided value is an :class:`~simplebench.simplebench_types.ElementCollection`
    of :class:`~simplebench.reporters.reporter.options.ReporterOptions` instances.

    An ElementCollection is a protocol representing a collection-like container (such as a list, set, or tuple)
    that supports iteration, length, and membership tests, but is not a mapping, string, or bytes.

    Returns a tuple containing the validated ReporterOptions instances. The order of the tuple is not guaranteed,
    as the input may be a set.

    If the input collection is empty, returns an empty tuple.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'options') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a collection of ReporterOptions instances.

    :return: A tuple of the validated ReporterOptions instances.
    :rtype: tuple[ReporterOptions, ...]
    """
    if not is_element_collection(value):
        message = f'Expected an ElementCollection of ReporterOptions instances for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_ARGS_NOT_NAMESPACE,
        )

    options_list: list[ReporterOptions] = []
    for item in value:
        if not isinstance(item, ReporterOptions):
            message = f'Expected all items in {field_name!r} to be ReporterOptions instances'
            raise SimpleBenchTypeError(
                message,
                tag=_ReporterErrorTag.VALIDATE_ARGS_NOT_NAMESPACE,
            )
        options_list.append(item)

    return tuple(options_list)


def config(value: Any, field_name: str = 'config') -> ReporterConfig:
    """Validate that the provided value is a :class:`~simplebench.reporters.reporter.config.ReporterConfig` instance.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'config') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a ReporterConfig instance.

    :return: The validated ReporterConfig instance.
    """
    if not isinstance(value, ReporterConfig):
        message = f'Expected a ReporterConfig instance for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.CONFIG_INVALID_ARG_TYPE,
        )
    return value


def case(value: Any, field_name: str = 'case') -> 'Case':
    """Validate that the provided value is a :class:`~simplebench.case.Case` instance.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'case') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a Case instance.

    :return: The validated Case instance.
    """
    if not is_case(value):
        message = f'Expected a Case instance for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.REPORT_INVALID_CASE_ARG,
        )
    return value


def choice(value: Any, field_name: str = 'choice') -> 'Choice':
    """Validate that the provided value is a :class:`~simplebench.reporters.choice.choice.Choice` instance.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'choice') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a Choice instance.

    :return: The validated Choice instance.
    """
    if not is_choice(value):
        message = f'Expected a Choice instance for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.REPORT_INVALID_CHOICE_ARG,
        )
    return value


def metrics_collection(value: Any, field_name: str = 'metrics_collection') -> MetricsCollection:
    """Validate that the provided value is a :class:`~simplebench.metrics.metrics.MetricsCollection` instance.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'metrics_collection') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a MetricsCollection instance.

    :return: The validated MetricsCollection instance.
    """
    if not isinstance(value, MetricsCollection):
        message = f'Expected a MetricsCollection instance for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.REPORT_NON_COLLECTION_METRICS_SELECTION,
        )
    return value

def supported_metrics(
            value: Any,
            supported_metrics: Set[Metric],
            field_name: str = 'choice.metrics') -> MetricsCollection:
    """Validate that the provided value is a :class:`~simplebench.metrics.metrics.MetricsCollection` instance
    and that it only contains supported Metrics.

    :param value: The metrics collection value to validate.
    :type value: Any
    :param field_name: (default = 'choice.metrics') The name of the field being validated, used in error messages.
    :type field_name: :class:`~simplebench.metrics.MetricsCollection`
    :param supported_metrics: The set of supported Metric instances.
    :type supported_metrics: Set[Metric]
    :raises SimpleBenchTypeError: If the provided value is not a MetricsCollection instance.
    :raises SimpleBenchValueError: If the MetricsCollection contains unsupported Metrics

    :return: The validated MetricsCollection instance.
    """
    if not isinstance(value, MetricsCollection):
        message = f'Expected a MetricsCollection instance for {field_name!r}: found {type(value).__name__}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.REPORT_NON_COLLECTION_METRICS_SELECTION,
        )
    metrics_set = set(value.metrics.values())
    unsupported_metrics = metrics_set - supported_metrics
    if unsupported_metrics:
        metrics_error = f'Unsupported Metric(s) in {field_name!r}: {unsupported_metrics}'
        raise SimpleBenchValueError(metrics_error, tag=_ReporterErrorTag.REPORT_UNSUPPORTED_METRICS)

    return value

def supported_targets(value: Any,
                      supported_targets: Set[Target],
                      field_name: str = 'choice.targets') -> frozenset[Target]:
    """Validate that the provided value is a Set of :class:`~simplebench.enums.Target` enums
    and that it only contains supported Targets.

    :param value: The targets value to validate.
    :type value: Any
    :param field_name: (default = 'choice.targets') The name of the field being validated, used in error messages.
    :type field_name: str
    :param supported_targets: The set of supported Target enums.
    :type supported_targets: Set[Target]
    :return: A validated frozenset of Target enums.
    :rtype: frozenset[Target]
    :raises SimpleBenchTypeError: If the provided value is not a Set of Target enums.
    :raises SimpleBenchValueError: If the Set contains unsupported Target enums.
    """
    if not isinstance(value, Set):
        message = f'Expected a Set of Target enums for {field_name!r}: found {type(value).__name__}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_INVALID_TARGETS_ARG_TYPE,
        )
    if not all(isinstance(t, Target) for t in value):
        message = f'Expected a Set of Target enums for {field_name!r}: found non-Target enum values'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_INVALID_TARGETS_ARG_VALUES,
        )
    if not isinstance(supported_targets, Set):
        raise SimpleBenchNotImplementedError(
            'supported_targets must be a Set of Target enums',
            tag=_ReporterErrorTag.VALIDATE_INVALID_SUPPORTED_TARGETS_ARG_TYPE,
        )
    if not all(isinstance(t, Target) for t in supported_targets):
        raise SimpleBenchNotImplementedError(
            'supported_targets must be a Set of Target enums',
            tag=_ReporterErrorTag.VALIDATE_INVALID_SUPPORTED_TARGETS_ARG_VALUES,
        )
    unsupported_targets = value - supported_targets
    if unsupported_targets:
        targets_error = f'Unsupported Target(s) in {field_name!r}: {unsupported_targets}'
        raise SimpleBenchValueError(targets_error, tag=_ReporterErrorTag.REPORT_UNSUPPORTED_TARGET)
    return frozenset(value)


def supported_formats(value: Any,
                      supported_formats: Set[Format],
                      field_name: str = 'choice.formats') -> frozenset[Format]:
    """Validate that the provided value is a Set of :class:`~simplebench.enums.Format` enums
    and that it only contains supported Formats.

    :param value: The formats value to validate.
    :type value: Any
    :param field_name: (default = 'choice.formats') The name of the field being validated, used in error messages.
    :type field_name: str
    :param supported_formats: The set of supported Format enums.
    :type supported_formats: Set[Format]
    :return: A validated frozenset of Format enums.
    :rtype: frozenset[Format]
    :raises SimpleBenchTypeError: If the provided value is not a Set of Format enums.
    :raises SimpleBenchValueError: If the Set contains unsupported Format enums.
    """
    if not isinstance(value, Set):
        message = f'Expected a Set of Format enums for {field_name!r}: found {type(value).__name__}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_INVALID_FORMATS_ARG_TYPE,
        )
    if not all(isinstance(f, Format) for f in value):
        message = f'Expected a Set of Format enums for {field_name!r}: found non-Format enum values'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_INVALID_FORMATS_ARG_VALUES,
        )
    if not isinstance(supported_formats, Set):
        raise SimpleBenchNotImplementedError(
            'supported_formats must be a Set of Format enums',
            tag=_ReporterErrorTag.VALIDATE_INVALID_SUPPORTED_FORMATS_ARG_TYPE,
        )
    if not all(isinstance(f, Format) for f in supported_formats):
        raise SimpleBenchNotImplementedError(
            'supported_formats must be a Set of Format enums',
            tag=_ReporterErrorTag.VALIDATE_INVALID_SUPPORTED_FORMATS_ARG_VALUES,
        )
    unsupported_formats = value - supported_formats
    if unsupported_formats:
        formats_error = f'Unsupported Format(s) in {field_name!r}: {unsupported_formats}'
        raise SimpleBenchValueError(formats_error, tag=_ReporterErrorTag.REPORT_UNSUPPORTED_FORMAT)
    return frozenset(value)


def path(value: Any, field_name: str = 'path') -> Path:
    """ Validate that the provided value is a :class:`~pathlib.Path` instance.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'path') The name of the field being validated, used in error messages.
    :type field_name: str
    :return: Validated Path instance.
    :rtype: :class:`~pathlib.Path`
    :raises SimpleBenchTypeError: If the provided value is not a :class:`~pathlib.Path` instance.
    """
    if not isinstance(value, Path):
        message = f'Expected a Path instance for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.REPORT_INVALID_PATH_ARG,
        )
    return value


def session(value: Any, field_name: str = 'session') -> Session:
    """Validate that the provided value is a :class:`~simplebench.session.session.Session` instance.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'session') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a Session instance.

    :return: The validated Session instance.
    """
    if not is_session(value):
        message = f'Expected a Session instance for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.REPORT_INVALID_SESSION_ARG,
        )
    return value


def callback_in_targets(value: Set[Target],
                        callback_value: ReporterCallback | None,
                        field_name: str = 'callback_in_targets',
                        ) -> None:
    """Validates that `value` is a Set of :class:`~simplebench.enum.target.Target` enums,
    and if the targets include :data:`~simplebench.enum.target.Target.CALLBACK`,
    then that the `callback_value` is a valid :class:`~simplebench.reporters.protocols.ReporterCallback`.

    If :data:`~simplebench.enum.target.Target.CALLBACK` is not in the targets in `value`,
    then the `callback_value` can be ``None``.

    :param value: A Set of Targets to validate
    :type value: Set[Target]
    :param callback_value: The ReporterCallback to validate if Target.CALLBACK is in targets.
    :type callback_value: ReporterCallback | None
    :param field_name: (default = 'callback_in_targets') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If `field_name` is not a string.
    :raises SimpleBenchTypeError: If the provided `value` is not a :class:`Set` of
        :class:`~simplebench.enum.target.Target`` enums.
    :raises SimpleBenchTypeError: If :data:`~simplebench.enum.target.Target.CALLBACK` is in `value` but
        `callback_value` is not a :class:`~simplebench.reporters.protocols.ReporterCallback` instance.
    :raises SimpleBenchTypeError: If callback_value is not ``None`` or
        a :class:`~simplebench.reporters.protocols.ReporterCallback` instance.
    """
    if not isinstance(value, Set):
        message = f'Expected a Set of Target enums for {field_name!r}: found {type(value).__name__}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_CALLBACK_IN_TARGETS_INVALID_TARGETS_ARG_TYPE,
        )
    if not all(isinstance(t, Target) for t in value):
        message = f'Expected a Set of Target enums for {field_name!r}: found non-Target enum values'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_CALLBACK_IN_TARGETS_INVALID_TARGETS_ARG_VALUE_TYPE,
        )
    if Target.CALLBACK in value:
        callback_value = callback(callback_value, field_name='callback_value')
        if callback_value is None:
            message = f'Target.CALLBACK specified in {field_name!r}, but no valid callback provided'
            raise SimpleBenchValueError(
                message,
                tag=_ReporterErrorTag.VALIDATE_NONE_CALLBACK_WITH_CALLBACK_TARGET)

def filesystem_in_targets(value: Set[Target],
                          path_value: Path | None,
                          field_name: str = 'filesystem_path') -> None:
    """Validate that if the `value` :class:`Set` of :class:`~simplebench.enum.targets.Targets`
    contains :data:`~simplebench.enum.target.Target.FILESYSTEM`, then `path` is a
    valid :class:`~pathlib.Path`.

    If :data:`~simplebench.enum.target.Target.FILESYSTEM` is not in `value`,
    then `path_value` is allowed to be ``None`` or :class:`~pathlib.Path`.

    :param value: The value to validate.
    :type value: :class:`~collections.abc.Set`[:class:`~simplebench.enum.target.Target`]
    :param path_value: The :class:`~pathlib.Path` to validate if
        :data:`~simplebench.enum.target.Target.FILESYSTEM` is in `value`.
    :type path_value: Path | None
    :param field_name: (default = 'filesystem_path') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provides `path_value` is not a :class:`~pathlib.Path` instance or :obj:`None`.
    :raises SimpleBenchTypeError: If the provided `value` is not a :class:`Set` containing only
        :class:`~simplebench.enum.target.Target` enums.
    :raises SimpleBenchValueError: If :data:`~simplebench.enum.target.Target.FILESYSTEM` is in `value`
        but `path_value` is ``None``.
    """
    if path_value is not None and not isinstance(path_value, Path):
        message = f'Expected a Path instance or None for `path_value` when validating {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_INVALID_FILESYSTEM_PATH_ARG_TYPE,
        )
    if not isinstance(value, Set):
        message = f'Expected a Set of Target enums for {field_name!r}: found {type(value).__name__}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_FILESYSTEM_IN_TARGETS_INVALID_TARGETS_ARG_TYPE,
        )
    if not all(isinstance(t, Target) for t in value):
        message = f'Expected a Set of Target enums for {field_name!r}: found non-Target enum values'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_FILESYSTEM_IN_TARGETS_INVALID_TARGETS_ARG_TYPE,
        )
    if Target.FILESYSTEM in value and path_value is None:
        message = f'Target.FILESYSTEM specified in {field_name!r}, but no path provided'
        raise SimpleBenchValueError(
            message,
            tag=_ReporterErrorTag.VALIDATE_INVALID_FILESYSTEM_PATH_ARG_TYPE,
        )


def callback(value: Any, field_name: str = 'callback') -> ReporterCallback | None:
    """Validate that the provided value is a :class:`~simplebench.reporters.protocols.ReporterCallback`
    instance or None.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'callback') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a ReporterCallback instance or None.

    :return: The validated ReporterCallback instance or None.
    """
    if value is not None and not isinstance(value, ReporterCallback):
        message = f'Expected a ReporterCallback instance or None for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.REPORT_INVALID_CALLBACK_ARG,
        )
    return value

def log_metadata(value: Any, field_name: str = 'log_metadata') -> Metadata:
    """Validate that the provided value is a :class:`~simplebench.metadata.Metadata` instance.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'log_metadata') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a Metadata instance.

    :return: The validated Metadata instance.
    """
    if not isinstance(value, Metadata):
        message = f'Expected a Metadata instance for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.REPORT_INVALID_LOG_METADATA_ARG,
        )
    return value

def reports_log_path(value: Metadata, field_name: str = 'log_metadata.reports_log_path') -> Path | None:
    """Validate that the provided value is a :class:`~simplebench.metadata.Metadata` instance
    and that its 'reports_log_path' property is either a :class:`~pathlib.Path` instance or ``None``.

    :param value: The value to validate.
    :type value: :class:`~simplebench.metadata.Metadata`
    :param field_name: (default = 'log_metadata.reports_log_path') The name of
        the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not a Metadata instance.
    :raises SimpleBenchTypeError: If the 'reports_log_path' property is not a :class:`~pathlib.Path`
        instance or ``None``.
    :return: A validated :class:`~pathlib.Path` instance or ``None``.
    :rtype: Path | None
    """
    metadata = log_metadata(value, field_name)
    if metadata.reports_log_path is None:
        return None
    if not isinstance(metadata.reports_log_path, Path):
        message = f'The "reports_log_path" property in {field_name!r} must be a Path instance or None'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.REPORT_INVALID_LOG_METADATA_ARG,
        )
    return metadata.reports_log_path

def args(value: Any, field_name: str = 'args') -> Namespace:
    """Validate that the provided value is an argparse.Namespace instance.

    :param value: The value to validate.
    :type value: Any
    :param field_name: (default = 'args') The name of the field being validated, used in error messages.
    :type field_name: str
    :raises SimpleBenchTypeError: If the provided value is not an argparse.Namespace instance.

    :return: The validated argparse.Namespace instance.
    """
    if not isinstance(value, Namespace):
        message = f'Expected an argparse.Namespace instance for {field_name!r}'
        raise SimpleBenchTypeError(
            message,
            tag=_ReporterErrorTag.VALIDATE_ARGS_NOT_NAMESPACE,
        )
    return value


def subclass_config(cls: type) -> None:
    """Validate that the subclass has correctly defined its options configuration.

    This method checks that the subclass has implemented the required class variables
    that allow the :class:`~.Reporter` base class to automatically instantiate the default
    options object.

    Subclasses must implement the following class variables:

        _OPTIONS_TYPE: ClassVar[type[MyOptions]] = MyOptions
        _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {...}

    ``_OPTIONS_TYPE`` must be a subclass of :class:`~.ReporterOptions`
    and ``_OPTIONS_KWARGS`` must be a ``dict[str, Any]`` that can be used
    to instantiate the ``_OPTIONS_TYPE`` subclass.

    :raises SimpleBenchNotImplementedError: If required class variables are not implemented
        or are of incorrect types.
    """
    from simplebench.reporters.reporter.reporter import Reporter

    # Verify that we are being called from a subclass of Reporter, not Reporter itself
    if cls is Reporter:
        raise SimpleBenchNotImplementedError(
            ('get_hardcoded_default_options() cannot be called directly on the Reporter class'),
            tag=_ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_CANNOT_BE_REPORTER,
        )
    if not issubclass(cls, Reporter):
        raise SimpleBenchNotImplementedError(
            ('Only sub-classes of Reporter can call get_hardcoded_default_options()'),
            tag=_ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_MUST_BE_SUBCLASS_OF_REPORTER,
        )

    # Verify that the subclass has implemented the _OPTIONS_TYPE class variable correctly
    # It must be implemented in the subclass, and it must be a subclass of ReporterOptions,
    # but not ReporterOptions itself
    if '_OPTIONS_TYPE' not in cls.__dict__:
        raise SimpleBenchNotImplementedError(
            (
                "Reporter subclasses must implement the class variable '_OPTIONS_TYPE' "
                'and set it to the specific ReporterOptions subclass they use'
            ),
            tag=_ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_NOT_IMPLEMENTED,
        )
    options = cls._OPTIONS_TYPE  # pylint: disable=no-member   # type: ignore[reportAttributeAccessIssue]
    if options is ReporterOptions:
        raise SimpleBenchNotImplementedError(
            (
                "Reporter subclasses must set '_OPTIONS_TYPE' to a ReporterOptions subclass, "
                'not the base ReporterOptions class'
            ),
            tag=_ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_INVALID_TYPE,
        )
    if not issubclass(options, ReporterOptions):
        raise SimpleBenchNotImplementedError(
            (
                "Reporter subclasses must implement the class variable '_OPTIONS_TYPE' "
                'and set it to a ReporterOptions subclass.'
            ),
            tag=_ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_MUST_BE_SUBCLASS,
        )

    # Verify the subclass has implemented the _OPTIONS_KWARGS class variable correctly
    # It must be implemented in the subclass, and it must be a dict[str, Any]
    if '_OPTIONS_KWARGS' not in cls.__dict__:
        raise SimpleBenchNotImplementedError(
            (
                "Reporter subclasses must implement the class variable '_OPTIONS_KWARGS' "
                'and set it to a dict of keyword arguments for the ReporterOptions subclass.'
            ),
            tag=_ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_NOT_IMPLEMENTED,
        )
    options_kwargs = cls._OPTIONS_KWARGS  # pylint: disable=no-member   # type: ignore[reportAttributeAccessIssue]
    if not isinstance(options_kwargs, dict):
        raise SimpleBenchNotImplementedError(
            (
                "Reporter subclasses must implement the class variable '_OPTIONS_KWARGS' "
                'and set it to a dict of keyword arguments for the ReporterOptions subclass.'
            ),
            tag=_ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_NOT_A_DICT,
        )
    if not all(isinstance(k, str) for k in options_kwargs.keys()):
        raise SimpleBenchNotImplementedError(
            ("Reporter subclasses must implement the class variable '_OPTIONS_KWARGS' as a dict with string keys."),
            tag=_ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_KEYS_MUST_BE_STR,
        )
