"""
Additional types module

Returns:
    GUID : GUID type
"""
import uuid

from sqlalchemy.types import CHAR, TypeDecorator


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        """
        Load dialect impl

        Args:
            dialect (Dialect): Dialect

        Returns:
            TypeEngine: Char typeEngine
        """
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        """
        Process bind parameters

        Args:
            value (parameter): Parameter vale
            dialect (parameter): Parameter dialect, optional

        Returns:
            str: UUID string
        """
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value
