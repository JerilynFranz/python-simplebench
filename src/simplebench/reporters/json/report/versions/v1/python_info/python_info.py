"""V1 PythonInfo implementation."""
import hashlib
import re
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.json.report.base import JSONSchema
from simplebench.reporters.json.report.base import PythonInfo as BasePythonInfo
from simplebench.reporters.json.report.exceptions import _PythonInfoErrorTag
from simplebench.validators import validate_string

from .python_info_schema import PythonInfoSchema


class PythonInfo(BasePythonInfo):
    """Class representing machine information in a JSON report."""

    TYPE: str = PythonInfoSchema.TYPE
    """The JSON PythonInfo type property value for version 1 reports."""

    VERSION: int = PythonInfoSchema.VERSION
    """The JSON PythonInfo version number."""

    ID: str = PythonInfoSchema.ID
    """The JSON PythonInfo identifier property value for version 1 reports."""

    SCHEMA: type[JSONSchema] = PythonInfoSchema
    """The JSON schema class for version 1 reports."""

    def __init__(self, *,
                 hash_id: str,
                 compiler: str,
                 implementation: str,
                 implementation_version: str,
                 python_version: str,
                 build: str,
                 release: str,
                 system: str) -> None:
        self.hash_id = hash_id
        self.compiler = compiler
        self.implementation = implementation
        self.implementation_version = implementation_version
        self.python_version = python_version
        self.build = build
        self.release = release
        self.system = system

    @property
    def compiler(self) -> str:
        """Get the compiler property.

        :return: The compiler string.
        """
        return self._compiler

    @compiler.setter
    def compiler(self, value: str) -> None:
        """Set the compiler property.

        It is validated to be a non-empty string.

        :param value: The compiler string to set.
        """
        self._compiler: str = validate_string(
            value, "compiler",
            _PythonInfoErrorTag.INVALID_COMPILER_PROPERTY_TYPE,
            _PythonInfoErrorTag.INVALID_COMPILER_PROPERTY_VALUE,
            strip=True, allow_empty=False)

    @property
    def implementation(self) -> str:
        """Get the implementation property.

        :return: The implementation string.
        """
        return self._implementation

    @implementation.setter
    def implementation(self, value: str) -> None:
        """Set the implementation property.

        It is validated to be a non-empty string.

        :param value: The implementation string to set.
        """
        self._implementation: str = validate_string(
            value, "implementation",
            _PythonInfoErrorTag.INVALID_IMPLEMENTATION_PROPERTY_TYPE,
            _PythonInfoErrorTag.INVALID_IMPLEMENTATION_PROPERTY_VALUE,
            strip=True, allow_empty=False)

    @property
    def implementation_version(self) -> str:
        """Get the implementation_version property.

        :return: The implementation_version string.
        """
        return self._implementation_version

    @implementation_version.setter
    def implementation_version(self, value: str) -> None:
        """Set the implementation_version property.

        It is validated to be a non-empty string.

        :param value: The implementation_version string to set.
        """
        self._implementation_version: str = validate_string(
            value, "implementation_version",
            _PythonInfoErrorTag.INVALID_IMPLEMENTATION_VERSION_PROPERTY_TYPE,
            _PythonInfoErrorTag.INVALID_IMPLEMENTATION_VERSION_PROPERTY_VALUE,
            strip=True, allow_empty=False)

    @property
    def python_version(self) -> str:
        """Get the python_version property.

        :return: The python_version string.
        """
        return self._python_version

    @python_version.setter
    def python_version(self, value: str) -> None:
        """Set the python_version property.

        It is validated to be a non-empty string.

        :param value: The python_version string to set.
        """
        self._python_version: str = validate_string(
            value, "python_version",
            _PythonInfoErrorTag.INVALID_PYTHON_VERSION_PROPERTY_TYPE,
            _PythonInfoErrorTag.INVALID_PYTHON_VERSION_PROPERTY_VALUE,
            strip=True, allow_empty=False)

    @property
    def build(self) -> str:
        """Get the build property.

        :return: The build string.
        """
        return self._build

    @build.setter
    def build(self, value: str) -> None:
        """Set the build property.

        It is validated to be a non-empty string.

        :param value: The build string to set.
        """
        self._build: str = validate_string(
            value, "build",
            _PythonInfoErrorTag.INVALID_BUILD_PROPERTY_TYPE,
            _PythonInfoErrorTag.INVALID_BUILD_PROPERTY_VALUE,
            strip=True, allow_empty=False)

    @property
    def release(self) -> str:
        """Get the release property.

        :return: The release string.
        """
        return self._release

    @release.setter
    def release(self, value: str) -> None:
        """Set the release property.

        It is validated to be a non-empty string.

        :param value: The release string to set.
        """
        self._release: str = validate_string(
            value, "release",
            _PythonInfoErrorTag.INVALID_RELEASE_PROPERTY_TYPE,
            _PythonInfoErrorTag.INVALID_RELEASE_PROPERTY_VALUE,
            strip=True, allow_empty=False)

    @property
    def system(self) -> str:
        """Get the system property.

        :return: The system string.
        """
        return self._system

    @system.setter
    def system(self, value: str) -> None:
        """Set the system property.

        It is validated to be a non-empty string.

        :param value: The system string to set.
        """
        self._system: str = validate_string(
            value, "system",
            _PythonInfoErrorTag.INVALID_SYSTEM_PROPERTY_TYPE,
            _PythonInfoErrorTag.INVALID_SYSTEM_PROPERTY_VALUE,
            strip=True, allow_empty=False)

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        if self._hash_id == '':
            # Get all __init__ params except 'hash_id' itself.
            # Sorting ensures a consistent order for hashing.
            hash_keys = sorted(k for k in self.init_params() if k != 'hash_id')

            # Create a null-byte separated string of "key:value" pairs.
            hash_input = "\x00".join(
                f"{key}:{getattr(self, key)}" for key in hash_keys
            ).encode('utf-8')

            self._hash_id = hashlib.sha256(hash_input).hexdigest()
        return self._hash_id

    @hash_id.setter
    def hash_id(self, value: str) -> None:
        """Set the hash_id property.

        It is validated to be a valid SHA-256 hexadecimal string or an empty string.

        :param value: The hash_id string to set.
        """
        hash_string = validate_string(
            value, "hash_id",
            _PythonInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
            _PythonInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
            allow_empty=True, strip=True)
        if hash_string == '':
            self._hash_id = ''
            return

        if not re.fullmatch(r'^[a-f0-9]{64}$', hash_string):
            raise SimpleBenchTypeError(
                "hash_id must be a valid SHA-256 hexadecimal string",
                tag=_PythonInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE)
        self._hash_id: str = hash_string

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'PythonInfo':
        """Create a PythonInfo instance from a dictionary.

        .. code-block:: python3
           :caption: Example

            python_info = PythonInfo.from_dict(data)

        The dictionary must conform to the expected structure for the PythonInfo
        representation. The 'version' and 'type' properties are validated
        against the class's VERSION and TYPE attributes if they are present.

        :param data: The dictionary containing PythonInfo information.
        :return: A PythonInfo instance.
        """
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str
        kwargs = cls.import_data(
            data=data,
            allowed=allowed_keys,
            skip={'version', 'type'},
            optional={'hash_id'},
            match_on={'version': cls.VERSION, 'type': cls.TYPE})
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the PythonInfo to a dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`PythonInfoSchema`
        for the version.

        :return: A dictionary representation of the PythonInfo.
        """
        property_keys = self.init_params().keys()
        data = {key: getattr(self, key) for key in property_keys}
        data['type'] = self.TYPE
        data['version'] = self.VERSION

        return data
