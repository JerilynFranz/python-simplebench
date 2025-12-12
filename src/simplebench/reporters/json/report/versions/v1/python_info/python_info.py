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

    def __init__(self,
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
            hash_input = (
                f"compiler:{self.compiler}\x00" +
                f"implementation:{self.implementation}\x00" +
                f"implementation_version:{self.implementation_version}\x00" +
                f"python_version:{self.python_version}\x00" +
                f"build:{self.build}\x00" +
                f"release:{self.release}\x00" +
                f"system:{self.system}"
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
        if not isinstance(data, dict):
            raise SimpleBenchTypeError(
                "data must be a dictionary",
                tag=_PythonInfoErrorTag.INVALID_DATA_ARG_TYPE)

        known_keys = {
            'hash_id',
            'compiler',
            'implementation',
            'implementation_version',
            'python_version',
            'build',
            'release',
            'system'
        }

        version = data.get('version') or cls.VERSION
        if not isinstance(version, int):
            raise SimpleBenchTypeError(
                "The 'version' property must be of type 'int' if set",
                tag=_PythonInfoErrorTag.INVALID_VERSION_TYPE)

        if version != cls.VERSION:
            raise SimpleBenchTypeError(
                f"The 'version' property must have the value {cls.VERSION} if set",
                tag=_PythonInfoErrorTag.UNSUPPORTED_VERSION)

        type_str = data.get('type') or cls.TYPE
        if not isinstance(type_str, str):
            raise SimpleBenchTypeError(
                "The 'type' property must be of type 'str' if set",
                tag=_PythonInfoErrorTag.INVALID_TYPE_TYPE)

        if type_str != cls.TYPE:
            raise SimpleBenchTypeError(
                f"The 'type' property must have tye value '{cls.TYPE}' if set",
                tag=_PythonInfoErrorTag.INVALID_TYPE_VALUE)

        extra_keys = set(data.keys()) - known_keys - {'version', 'type'}
        if extra_keys:
            raise SimpleBenchTypeError(
                f"Unexpected keys in data dictionary: {extra_keys}",
                tag=_PythonInfoErrorTag.INVALID_DATA_ARG_EXTRA_KEYS)
        missing_keys = known_keys - data.keys() - {'hash_id'}
        if missing_keys:
            raise SimpleBenchTypeError(
                f"Missing required keys in data dictionary: {missing_keys}",
                tag=_PythonInfoErrorTag.INVALID_DATA_ARG_MISSING_KEYS)

        instance = cls(
            hash_id=data.get('hash_id', ''),
            compiler=data['compiler'],
            implementation=data['implementation'],
            implementation_version=data['implementation_version'],
            python_version=data['python_version'],
            build=data['build'],
            release=data['release'],
            system=data['system']
        )

        return instance

    def to_dict(self) -> dict[str, Any]:
        """Convert the PythonInfo to a dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`PythonInfoSchema`
        for the version.

        :return: A dictionary representation of the PythonInfo.
        """
        cls = self.__class__
        result: dict[str, Any] = {
            'version': cls.VERSION,
            'type': cls.TYPE,
            'hash_id': self.hash_id,
            'compiler': self.compiler,
            'implementation': self.implementation,
            'implementation_version': self.implementation_version,
            'python_version': self.python_version,
            'build': self.build,
            'release': self.release,
            'system': self.system
        }
        return result
