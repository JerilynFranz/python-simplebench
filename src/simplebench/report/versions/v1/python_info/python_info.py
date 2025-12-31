"""V1 PythonInfo implementation."""
import hashlib

from simplebench.report._base import BasePythonInfo, JSONSchema
from simplebench.report.versions.v1.types import PythonInfoData, PythonInfoDict

from . import validate
from .python_info_schema import PythonInfoSchema


class PythonInfo(BasePythonInfo):
    """Class representing python execution environment in a report (V1)."""

    SCHEMA: type[JSONSchema] = PythonInfoSchema
    """The JSON schema class for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON PythonInfo type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON PythonInfo version number."""

    ID: str = SCHEMA.ID
    """The JSON PythonInfo identifier property value for version 1 reports."""

    def __init__(self, *,
                 hash_id: str,
                 compiler: str,
                 implementation: str,
                 implementation_version: str,
                 python_version: str,
                 build: str,
                 release: str,
                 system: str) -> None:
        self._hash_id = validate.hash_id(hash_id)
        self._compiler = validate.compiler(compiler)
        self._implementation = validate.implementation(implementation)
        self._implementation_version = validate.implementation_version(implementation_version)
        self._python_version = validate.python_version(python_version)
        self._build = validate.build(build)
        self._release = validate.release(release)
        self._system = validate.system(system)

    @classmethod
    def from_dict(cls, data: PythonInfoData) -> 'PythonInfo':
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
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'hash_id', 'version', 'type'},
            defaults={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE})
        return cls(**kwargs)

    def to_dict(self) -> PythonInfoDict:
        """Convert the PythonInfo to a dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`PythonInfoSchema`
        for the version.

        :return PythonInfoDict: A dictionary representation of the PythonInfo.
        """
        cls = self.__class__
        return PythonInfoDict(
            type=cls.TYPE,
            version=cls.VERSION,
            hash_id=self.hash_id,
            compiler=self.compiler,
            implementation=self.implementation,
            implementation_version=self.implementation_version,
            python_version=self.python_version,
            build=self.build,
            release=self.release,
            system=self.system
        )

    @property
    def compiler(self) -> str:
        """Get the compiler property.

        :return: The compiler string.
        """
        return self._compiler

    @property
    def implementation(self) -> str:
        """Get the implementation property.

        :return: The implementation string.
        """
        return self._implementation

    @property
    def implementation_version(self) -> str:
        """Get the implementation_version property.

        :return: The implementation_version string.
        """
        return self._implementation_version

    @property
    def python_version(self) -> str:
        """Get the python_version property.

        :return: The python_version string.
        """
        return self._python_version

    @property
    def build(self) -> str:
        """Get the build property.

        :return: The build string.
        """
        return self._build

    @property
    def release(self) -> str:
        """Get the release property.

        :return: The release string.
        """
        return self._release

    @property
    def system(self) -> str:
        """Get the system property.

        :return: The system string.
        """
        return self._system

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
