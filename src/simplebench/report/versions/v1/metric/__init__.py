"""Metric module for SimpleBench report version 1."""
# ruff: noqa: F401
from .metric import Metric
from .metric_schema import MetricSchema
from .typed_dict import ImmutableMetricData, ImmutableMetricDict, MetricData, MetricDict

__all__: list[str] = []
