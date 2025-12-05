"""Log reporter schemas package."""
from .v1 import LogReportMetadataSchema as v1

log_report_schemas = {
    1: v1,
}

LATEST_SCHEMA_VERSION = max(log_report_schemas.keys())
