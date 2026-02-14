"""TypedDict definitions for the Generic Environment report."""
from collections.abc import Mapping

__all__: list[str] = []

from simplebench.report.base import ReportElementTypedDict
from simplebench.simplebench_types import CoreDataMapping, CoreDataTypes, Never, NotRequired, Required

# --- For data used as INPUT (e.g., to `from_dict`) ---

class EnvironmentData(ReportElementTypedDict):
    """TypedDict for the Environment data.

    This TypedDict represents the structure of the 'data' field in the Environment report.
    The keys are expected to be strings that match the pattern defined in the JSON schema, and
    the values can be of various types, including nested dictionaries, strings, numbers, booleans, nulls, or arrays.

    :param version: The JSON Environment version number.
    :type version: NotRequired[str]
    :param type: The JSON Environment type property value for version 1 reports.
    :type type: NotRequired[str]
    :param hash_id: Unique 64 byte hexadecimal hash identifier for the Environment data.
        This can be used to identify the generator and uniqueness of the data.
    :type hash_id: NotRequired[str]
    :param semantic_type: The semantic type of the environment, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace.
    :type semantic_type: Required[str]
    :param data: The raw Environment data collected from the system.
    :type data: Required[Mapping[str, CoreDataTypes]]
    """
    version: NotRequired[str]
    type: NotRequired[str]
    hash_id: NotRequired[str]
    semantic_type: Required[str]
    data: Required[Mapping[str, CoreDataTypes]]


class ImmutableEnvironmentData(ReportElementTypedDict):
    """Immutable TypedDict for the Environment data.

    This TypedDict represents the structure of the 'data' field in the Environment report.
    The keys are expected to be strings that match the pattern defined in the JSON schema, and
    the values can be of various types, including nested dictionaries, strings, numbers, booleans, nulls, or arrays.

    :param version: The JSON Environment version number.
    :type version: NotRequired[str]
    :param type: The JSON Environment type property value for version 1 reports.
    :type type: NotRequired[str]
    :param hash_id: Unique 64 byte hexadecimal hash identifier for the Environment data.
        This can be used to identify the generator and uniqueness of the data.
    :type hash_id: NotRequired[str]
    :param semantic_type: The semantic type of the environment, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace.
    :type semantic_type: Required[str]
    :param data: The raw Environment data collected from the system.
    :type data: Required[CoreDataMapping]
    """
    version: NotRequired[str]
    type: NotRequired[str]
    hash_id: NotRequired[str]
    semantic_type: Required[str]
    data: Required[CoreDataMapping]
    __immutable__: NotRequired[Never]  # Class marker to indicate immutability

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class EnvironmentDict(ReportElementTypedDict):
    """TypedDict for the Environment data.

    This TypedDict represents the structure of the 'data' field in the Environment report.
    The keys are expected to be strings that match the pattern defined in the JSON schema, and
    the values can be of various types, including nested dictionaries, strings, numbers, booleans,
    nulls, or arrays.

    :param version: The JSON Environment version number.
    :type version: Required[str]
    :param type: The JSON Environment type property value for version 1 reports.
    :type type: Required[str]
    :param hash_id: Unique 64 byte hexadecimal hash identifier for the Environment data.
        This can be used to identify the generator and uniqueness of the data.
    :type hash_id: Required[str]
    :param semantic_type: The semantic type of the environment, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace.
    :type semantic_type: Required[str]
    :param data: The raw Environment data collected from the system.
    :type data: Required[Mapping[str, CoreDataTypes]]
    """
    version: Required[str]
    type: Required[str]
    hash_id: Required[str]
    semantic_type: Required[str]
    data: Required[Mapping[str, CoreDataTypes]]


class ImmutableEnvironmentDict(ReportElementTypedDict):
    """Immutable TypedDict for the Environment data.

    This TypedDict represents the structure of the 'data' field in the Environment report.
    The keys are expected to be strings that match the pattern defined in the JSON schema, and
    the values can be of various types, including nested dictionaries, strings, numbers, booleans,
    nulls, or arrays.

    :param version: The JSON Environment version number.
    :type version: Required[str]
    :param type: The JSON Environment type property value for version 1 reports.
    :type type: Required[str]
    :param hash_id: Unique 64 byte hexadecimal hash identifier for the Environment data.
        This can be used to identify the generator and uniqueness of the data.
    :type hash_id: Required[str]
    :param semantic_type: The semantic type of the environment, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace.
    :type semantic_type: Required[str]
    :param data: The raw Environment data collected from the system.
    :type data: Required[CoreDataMapping]
    """
    version: Required[str]
    type: Required[str]
    hash_id: Required[str]
    semantic_type: Required[str]
    data: Required[CoreDataMapping]
    __immutable__: NotRequired[Never]  # Class marker to indicate immutability
