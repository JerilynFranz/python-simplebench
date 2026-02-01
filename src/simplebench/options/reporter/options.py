"""Base class for reporter-specific options."""

__all__: list[str] = []


class ReporterOptions:
    """Marker base class for reporter related options.

    This class serves as a base for all reporter-specific options classes
    used within the simplebench framework. It provides a common base type
    for all reporter options.

    These options classes can be used to encapsulate configuration settings
    specific to different reporter implementations and are typically used
    in Choice() and Case() objects to customize reporter behavior.
    """
