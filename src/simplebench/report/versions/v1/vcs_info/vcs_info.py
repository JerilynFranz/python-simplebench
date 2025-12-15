"""VCSInfo version 1 base class.

This class represents vcs information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/vcs-info.json

It is the base implemention of the JSON report vcs info representation.

This makes the implementations of VCSInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base VCSInfo representation at the time of the V1 schema release.
"""
import hashlib
import re
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _VCSInfoErrorTag
from simplebench.report.base import JSONSchema
from simplebench.report.base import VCSInfo as BaseVCSInfo
from simplebench.validators import validate_string

from .vcs_info_schema import VCSInfoSchema


class VCSInfo(BaseVCSInfo):
    """Class representing vcs information in a JSON report."""

    TYPE: str = VCSInfoSchema.TYPE
    """The JSON VCSInfo type property value for version 1 reports."""

    VERSION: int = VCSInfoSchema.VERSION
    """The JSON VCSInfo version number."""

    ID: str = VCSInfoSchema.ID
    """The JSON VCSInfo schema identifier for version 1 reports."""

    SCHEMA: type[JSONSchema] = VCSInfoSchema
    """The JSON schema class for version 1 reports."""

    def __init__(self,
                 *,
                 hash_id: str = '',
                 ) -> None:
        """Initialize JSONVCSInfo.

        :param hash_id: The unique hash identifier for the machine information.
            If not provided, it defaults to an empty string and will be computed automatically.
        """
        self.hash_id = hash_id

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        if self._hash_id == '':
            hash_keys = sorted(k for k in self.init_params() if k != 'hash_id')

            def get_val(key: str) -> Any:
                value = getattr(self, key)
                if hasattr(value, 'hash_id'):
                    return value.hash_id
                return value

            hash_input = "\x00".join(
                f"{key}:{get_val(key)}" for key in hash_keys
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
            _VCSInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
            _VCSInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
            allow_empty=True, strip=True)
        if hash_string == '':
            self._hash_id = ''
            return

        if not re.fullmatch(r'^[a-f0-9]{64}$', hash_string):
            raise SimpleBenchTypeError(
                "hash_id must be a valid SHA-256 hexadecimal string",
                tag=_VCSInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE)
        self._hash_id: str = hash_string

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'VCSInfo':
        """Create a VCSInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           vcs_info = VCSInfo.from_dict(data)

        :param data: The dictionary containing vcs information.
        :return: A VCSInfo instance.
        """
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        kwargs = cls.import_data(
            data=data,
            allowed=allowed_keys,
            skip={'version', 'type'},
            optional={'hash_id', 'version', 'type'},
            default={'hash_id': '', 'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE})
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the VCSInfo to a dictionary.

        :return: A dictionary representation of the VCSInfo.
        """
        data: dict[str, Any] = {}
        for key in self.init_params():
            value = getattr(self, key)
            if hasattr(value, 'to_dict'):
                data[key] = value.to_dict()
            else:
                data[key] = value

        data['type'] = self.TYPE
        data['version'] = self.VERSION
        return data
