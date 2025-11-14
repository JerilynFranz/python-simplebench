"""Options for a MatPlotLib graph reporter in the reporters package.

These options are used to configure the behavior of a MatPlotLib reporter
when generating graph reports for benchmark test cases."""
from typing import ClassVar
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.validators import validate_int_range, validate_type, validate_float, validate_bool

# simplebench.reporters.graph imports
from simplebench.reporters.graph.options import GraphOptions
from simplebench.reporters.graph.enums.image_type import ImageType

# simplebench.reporters.graph.matplotlib imports
from ..enums.style import Style
from ..theme import Theme, DefaultTheme

# simplebench.reporters.graph.matplotlib.options imports
from .exceptions import MatPlotLibOptionsErrorTag


class MatPlotLibOptions(GraphOptions):
    """Class for holding MatPlotLib graph reporter specific options.
    This class extends the `GraphOptions` interface and forms a new interface
    for options specific to MatPlotLib-based graph reporters.

    It makes it easy to create graph reporters with MatPlotLib by providing
    a standard set of options that can be used across multiple reporters via
    subclassing.

    It includes the defaults for various MatPlotLib reporter defaults that can be
    set globally for all MatPlotLib reporters via static methods, as well as instance-specific
    options that can be set when creating a MatPlotLibOptions instance or when creating
    a benchmark test case.

    The philosophy behind having both static/global defaults and instance-specific options
    is to provide flexibility in configuration in a 'simple things should be simple, complex
    things should be possible' manner.

    Users can set global defaults that apply to all MatPlotLib reporters, ensuring easy
    consistency across reports. At the same time, instance-specific options allow
    for customization on a per-report basis, enabling users to tailor the behavior of
    individual reports as needed.

    The baseline defaults provided here are intended to offer a good balance between
    quality, appearance, and performance for most common use cases.

    Those defaults are as follows:
        - Width: `1500` pixels
        - Height: `750` pixels
        - DPI: `150`
        - Y-axis starts at zero: `True`
        - X-axis labels rotation: `45.0` degrees
        - Style: `Style.DARK_BACKGROUND`
        - Theme: `theme.DefaultTheme`
        - ImageType: `ImageType.SVG`

        These defaults are used both by Case instances when creating reports for specific test cases and by
        Choice instances when creating reports for all test cases under that Choice.

        The semantics are that Case.options take precedence over Choice.options take precedence
        over the class defaults. This allows for flexible configuration at multiple levels.

    Attributes:
        width (int): The default width of the MatPlotLib output in pixels when rendered.
        height (int): The default height of the MatPlotLib output in pixels when rendered.
        dpi (int): The default DPI (dots per inch) for the MatPlotLib output when rendered.
        y_starts_at_zero (bool): The default for whether the Y-axis for graphs should start at zero.
        x_labels_rotation (float): The default rotation angle in degrees for X-axis labels.
        style (Style): The default style for the MatPlotLib graphs.
        theme (Theme): The default theme to use for the MatPlotLib graphs.
        image_type (ImageType): The output image format for the graph files.
    """
    _HARDCODED_DEFAULT_WIDTH: ClassVar[int] = 1500
    """Hardcoded default width in pixels for all MatPlotLib graphs.
    (private class attribute)"""
    _HARDCODED_DEFAULT_HEIGHT: ClassVar[int] = 750
    """Hardcoded default height in pixels for all MatPlotLib graphs.
    (private class attribute)"""
    _HARDCODED_DEFAULT_DPI: ClassVar[int] = 150
    """Hardcoded default DPI for all MatPlotLib graphs.
    (private class attribute)"""
    _HARDCODED_DEFAULT_Y_STARTS_AT_ZERO: ClassVar[bool] = True
    """Hardcoded default value for whether Y-axis starts at zero for all MatPlotLib graphs.
    (private class attribute)"""
    _HARDCODED_DEFAULT_X_LABELS_ROTATION: ClassVar[float] = 45.0
    """Hardcoded default rotation angle in degrees for X-axis labels for all MatPlotLib graphs.
    (private class attribute)"""
    _HARDCODED_DEFAULT_STYLE: ClassVar[Style] = Style.DARK_BACKGROUND
    """Hardcoded default style for all MatPlotLib graphs.
    (private class attribute)"""
    _HARDCODED_DEFAULT_THEME: ClassVar[Theme] = DefaultTheme
    """Hardcoded default theme for all MatPlotLib graphs.
    (private class attribute)"""
    _HARDCODED_IMAGE_TYPE: ClassVar[ImageType] = ImageType.SVG
    """Hardcoded default image type for all MatPlotLib graphs.
    (private class attribute)"""

    DEFAULT_KWARGS: ClassVar[dict[str, object]] = {
        'width': _HARDCODED_DEFAULT_WIDTH,
        'height': _HARDCODED_DEFAULT_HEIGHT,
        'dpi': _HARDCODED_DEFAULT_DPI,
        'y_starts_at_zero': _HARDCODED_DEFAULT_Y_STARTS_AT_ZERO,
        'x_labels_rotation': _HARDCODED_DEFAULT_X_LABELS_ROTATION,
        'style': _HARDCODED_DEFAULT_STYLE,
        'theme': _HARDCODED_DEFAULT_THEME,
        'image_type': _HARDCODED_IMAGE_TYPE,
    }
    """Default keyword arguments for MatPlotLibOptions constructor.
        - width: int = 1500
        - height: int = 750
        - dpi: int = 150
        - y_starts_at_zero: bool = True
        - x_labels_rotation: float = 45.0
        - style: Style = Style.DARK_BACKGROUND
        - theme: Theme = Theme.Default
        - image_type: ImageType = ImageType.SVG
    """

    @classmethod
    def get_hardcoded_default_width(cls) -> int:
        """Return the hardcoded default width in pixels for all MatPlotLib graphs.

        Returns:
            int: The hardcoded default width in pixels for all MatPlotLib graphs.
        """
        return cls._HARDCODED_DEFAULT_WIDTH

    @classmethod
    def get_hardcoded_default_height(cls) -> int:
        """Return the hardcoded default height in pixels for all MatPlotLib graphs.

        Returns:
            int: The hardcoded default height in pixels for all MatPlotLib graphs.
        """
        return cls._HARDCODED_DEFAULT_HEIGHT

    @classmethod
    def get_hardcoded_default_dpi(cls) -> int:
        """Return the hardcoded default DPI for all MatPlotLib graphs.

        Returns:
            int: The hardcoded default DPI for all MatPlotLib graphs.
        """
        return cls._HARDCODED_DEFAULT_DPI

    @classmethod
    def get_hardcoded_default_y_starts_at_zero(cls) -> bool:
        """Return the hardcoded default value for whether Y-axis starts at zero for all MatPlotLib graphs.

        Returns:
            bool: The hardcoded default value for whether Y-axis starts at zero for all MatPlotLib graphs.
        """
        return cls._HARDCODED_DEFAULT_Y_STARTS_AT_ZERO

    @classmethod
    def get_hardcoded_default_x_labels_rotation(cls) -> float:
        """Return the hardcoded default rotation angle in degrees for X-axis labels for all MatPlotLib graphs.

        Returns:
            float: The hardcoded default rotation angle in degrees for X-axis labels for all MatPlotLib graphs.
        """
        return cls._HARDCODED_DEFAULT_X_LABELS_ROTATION

    @classmethod
    def get_hardcoded_default_style(cls) -> Style:
        """Return the hardcoded default style for all MatPlotLib graphs.

        Returns:
            Style: The hardcoded default style for all MatPlotLib graphs.
        """
        return cls._HARDCODED_DEFAULT_STYLE

    @classmethod
    def get_hardcoded_default_theme(cls) -> Theme:
        """Return the hardcoded default theme for all MatPlotLib graphs.

        Returns:
            Theme: The hardcoded default theme for all MatPlotLib graphs.
        """
        return cls._HARDCODED_DEFAULT_THEME

    @classmethod
    def get_hardcoded_default_image_type(cls) -> ImageType:
        """Return the hardcoded default image type for all MatPlotLib graphs.

        Returns:
            ImageType: The hardcoded default image type for all MatPlotLib graphs.
        """
        return cls._HARDCODED_IMAGE_TYPE

    _DEFAULT_WIDTH: int | None = None
    """Default width in pixels for all MatPlotLib graphs (private class attribute)"""
    @classmethod
    def set_default_width(cls, width: int | None) -> None:
        """Set the default width in pixels for all MatPlotLib graphs.

        Args:
            width (int | None): The width to set as the default for MatPlotLib graphs.
                If set None, the built-in hardcoded default width will be restored.
                The width must be between 500 and 4000 pixels.

        Raises:
            SimbleBenchTypeError: If the width is not an integer or None.
            SimbleBenchValueError: If the width is not within the valid range.
        """
        cls._DEFAULT_WIDTH = validate_int_range(
            width, 'MatPlotLibOptions.width',
            MatPlotLibOptionsErrorTag.INVALID_DEFAULT_WIDTH_ARG_TYPE,
            MatPlotLibOptionsErrorTag.INVALID_DEFAULT_WIDTH_ARG_VALUE,
            min_value=500, max_value=4000) if width is not None else None

    @classmethod
    def get_default_width(cls) -> int:
        """Return the default width in pixels for all MatPlotLib graphs.

        If no default width has been explicitly set, then
        it returns the hardcoded default width of 1500.

        Returns:
            int: The default width in pixels for all MatPlotLib graphs.
        """
        if cls._DEFAULT_WIDTH is None:
            return cls._HARDCODED_DEFAULT_WIDTH
        return cls._DEFAULT_WIDTH

    _DEFAULT_HEIGHT: int | None = None
    """Default height in pixels for all MatPlotLib graphs (private class attribute)"""
    @classmethod
    def set_default_height(cls, height: int | None) -> None:
        """Set the default height in pixels for all MatPlotLib graphs.

        If height is set to None, the built-in hardcoded default height will be restored.

        Args:
            height (int | None): The height to set as the default for MatPlotLib graphs.
                If None, the built-in default height will be used. The height must be between
                500 and 4000 pixels.

        Raises:
            SimbleBenchTypeError: If the height is not an integer or None.
            SimbleBenchValueError: If the height is not within the valid range.
        """
        cls._DEFAULT_HEIGHT = validate_int_range(
            height, 'height',
            MatPlotLibOptionsErrorTag.INVALID_DEFAULT_HEIGHT_ARG_TYPE,
            MatPlotLibOptionsErrorTag.INVALID_DEFAULT_HEIGHT_ARG_VALUE,
            min_value=500, max_value=4000) if height is not None else None

    @classmethod
    def get_default_height(cls) -> int:
        """Return the default height in pixels for all MatPlotLib graphs.

        If no default height has been explicitly set, returns the hardcoded default
        height of 750.

        Returns:
            int: The default height in pixels for all MatPlotLib graphs.
        """
        if cls._DEFAULT_HEIGHT is None:
            return cls._HARDCODED_DEFAULT_HEIGHT
        return cls._DEFAULT_HEIGHT

    _DEFAULT_DPI: int | None = None
    """Default DPI for all MatPlotLib graphs (private class attribute)"""
    @classmethod
    def set_default_dpi(cls, dpi: int | None) -> None:
        """Set the default DPI for all MatPlotLib graphs.

        If dpi is set to None, the built-in hardcoded default DPI will be restored.

        Args:
            dpi (int | None): The DPI to set as the default for MatPlotLib graphs.
                If None, the built-in default DPI will be used. The DPI must be between
                50 and 400.

        Raises:
            SimbleBenchTypeError: If the dpi is not an integer or None.
            SimbleBenchValueError: If the dpi is not within the valid range.
        """
        cls._DEFAULT_DPI = validate_int_range(
            dpi, 'dpi',
            MatPlotLibOptionsErrorTag.INVALID_DEFAULT_DPI_ARG_TYPE,
            MatPlotLibOptionsErrorTag.INVALID_DEFAULT_DPI_ARG_VALUE,
            min_value=50, max_value=400) if dpi is not None else None

    @classmethod
    def get_default_dpi(cls) -> int:
        """Return the default DPI for all MatPlotLib graphs.

        If no default DPI has been explicitly set, returns the hardcoded default
        DPI of 150.

        Returns:
            int: The default DPI for all MatPlotLib graphs.
        """
        if cls._DEFAULT_DPI is None:
            return cls._HARDCODED_DEFAULT_DPI
        return cls._DEFAULT_DPI

    _DEFAULT_Y_STARTS_AT_ZERO: bool | None = None
    """Default value for whether Y-axis starts at zero for all MatPlotLib graphs. (private class attribute)."""
    @classmethod
    def set_default_y_starts_at_zero(cls, y_starts_at_zero: bool | None) -> None:
        """Set the default value for whether Y-axis starts at zero for all MatPlotLib graphs

        Setting this to None will restore the default hardcoded setting of starting the Y-axis at zero.

        Args:
            y_starts_at_zero (bool | None): The value to set as the default for MatPlotLib graphs.

        Raises:
            SimpleBenchTypeError: If y_starts_at_zero is not a bool or None.
        """
        if y_starts_at_zero is not None and not isinstance(y_starts_at_zero, bool):
            raise SimpleBenchTypeError(
                'default_y_starts_at_zero must be a bool or None.',
                tag=MatPlotLibOptionsErrorTag.INVALID_Y_STARTS_AT_ZERO_ARG_TYPE)
        cls._DEFAULT_Y_STARTS_AT_ZERO = y_starts_at_zero

    @classmethod
    def get_default_y_starts_at_zero(cls) -> bool:
        """Return the default value for whether Y-axis starts at zero for all MatPlotLib graphs.

        If no default has been explicitly set, returns the hardcoded built-in default of True.

        Returns:
            bool: The default value for whether Y-axis starts at zero for all MatPlotLib graphs.
        """
        if cls._DEFAULT_Y_STARTS_AT_ZERO is None:
            return cls._HARDCODED_DEFAULT_Y_STARTS_AT_ZERO
        return cls._DEFAULT_Y_STARTS_AT_ZERO

    _DEFAULT_X_LABELS_ROTATION: float | None = None
    """Default rotation angle in degrees for X-axis labels for all MatPlotLib graphs (private class attribute)."""
    @classmethod
    def set_default_x_labels_rotation(cls, x_labels_rotation: float | None) -> None:
        """Set the default rotation angle in degrees for X-axis labels for all MatPlotLib graphs.

        Setting this to None will restore the default rotation angle of 45.0 degrees.

        Args:
            x_labels_rotation (float | None): The rotation angle to set as the default for MatPlotLib graphs.

        Raises:
            SimpleBenchTypeError: If x_labels_rotation is not a float or None.
        """
        if x_labels_rotation is not None and not isinstance(x_labels_rotation, (int, float)):
            raise SimpleBenchTypeError(
                'MatPlotLibOptions.default_x_labels_rotation must be a float or None.',
                tag=MatPlotLibOptionsErrorTag.INVALID_DEFAULT_X_LABELS_ROTATION_ARG_TYPE)
        MatPlotLibOptions._DEFAULT_X_LABELS_ROTATION = x_labels_rotation

    @classmethod
    def get_default_x_labels_rotation(cls) -> float:
        """Return the default rotation angle in degrees for X-axis labels for all MatPlotLib graphs.

        If no default has been explicitly set, returns the hardcoded built-in default of 45.0 degrees.

        Returns:
            float: The default rotation angle in degrees for X-axis labels for all MatPlotLib graphs.
        """
        if cls._DEFAULT_X_LABELS_ROTATION is None:
            return cls._HARDCODED_DEFAULT_X_LABELS_ROTATION
        return cls._DEFAULT_X_LABELS_ROTATION

    _DEFAULT_STYLE: Style | None = None
    """Default style/theme for all MatPlotLib graphs (private class attribute)."""
    @classmethod
    def set_default_style(cls, style: Style | None = None) -> None:
        """Set the default style/theme for all MatPlotLib graphs.

        This static method allows setting a global default style for all MatPlotLib graphs.
        If set to None, the build-in hardcoded default MatPlotLib style will be used.

        Args:
            style (Style | None, default=None): The style to set as the default for MatPlotLib graphs.

        Raises:
            SimpleBenchTypeError: If the style is not a Style enum member or None.
        """
        if style is not None and not isinstance(style, Style):
            raise SimpleBenchTypeError(
                'MatPlotLibOptions.default_style must be a Style value or None.',
                tag=MatPlotLibOptionsErrorTag.INVALID_DEFAULT_STYLE_ARG_TYPE)
        cls._DEFAULT_STYLE = style

    @classmethod
    def get_default_style(cls) -> Style:
        """Return the default style for MatPlotLib graphs.

        If no default style has been explictly set, returns the hardcoded
        built-in Style.DARK_BACKGROUND.

        Returns:
            Style: The default style for MatPlotLib graphs.
        """
        if cls._DEFAULT_STYLE is None:
            return cls._HARDCODED_DEFAULT_STYLE
        return cls._DEFAULT_STYLE

    _DEFAULT_THEME: Theme | None = None
    """Default theme for all MatPlotLib graphs (private class attribute)."""
    @classmethod
    def set_default_theme(cls, theme: Theme | None = None) -> None:
        """Set the default theme for all MatPlotLib graphs.

        This static method allows setting a global default theme for all MatPlotLib graphs.
        If set to None, the built-in hardcoded default MatPlotLib theme (`DefaultTheme`)
        will be used.

        Args:
            theme (Theme | None, default=None): The theme to set as the default for MatPlotLib graphs.

        Raises:
            SimpleBenchTypeError: If the theme is not a Theme instance or None.
        """
        if theme is not None and not isinstance(theme, Theme):
            raise SimpleBenchTypeError(
                'MatPlotLibOptions.default_theme must be a Theme instance or None.',
                tag=MatPlotLibOptionsErrorTag.INVALID_DEFAULT_THEME_ARG_TYPE)
        cls._DEFAULT_THEME = theme

    @classmethod
    def get_default_theme(cls) -> Theme:
        """Return the default theme for MatPlotLib graphs.

        If no default theme has been explictly set, returns Default.

        Returns:
            Theme: The default theme for MatPlotLib graphs.
        """
        if cls._DEFAULT_THEME is None:
            return cls._HARDCODED_DEFAULT_THEME
        return cls._DEFAULT_THEME

    _DEFAULT_IMAGE_TYPE: ImageType | None = None
    """Default image type for all MatPlotLib graphs (private class attribute)."""
    @staticmethod
    def set_default_image_type(image_type: ImageType | None) -> None:
        """Set the default image type for all MatPlotLib graphs.

        If image_type is set to None, the built-in default image type will be restored.

        Args:
            image_type (ImageType | None): The image type to set as the default for MatPlotLib graphs.
                If None, the built-in default image type will be used.

        Raises:
            SimpleBenchTypeError: If the image_type is not an ImageType enum member or None.
        """
        MatPlotLibOptions._DEFAULT_IMAGE_TYPE = image_type

    @staticmethod
    def get_default_image_type() -> ImageType:
        """Return the default image type for all MatPlotLib graphs.

        If no default image type has been explicitly set, returns ImageType.SVG.

        Returns:
            ImageType: The default image type for all MatPlotLib graphs.
        """
        if MatPlotLibOptions._DEFAULT_IMAGE_TYPE is None:
            return ImageType.SVG
        return MatPlotLibOptions._DEFAULT_IMAGE_TYPE

    def __init__(self,
                 width: int | None = None,
                 height: int | None = None,
                 dpi: int | None = None,
                 y_starts_at_zero: bool | None = None,
                 x_labels_rotation: float | None = None,
                 style: Style | None = None,
                 theme: Theme | None = None,
                 image_type: ImageType | None = None,
                 ) -> None:
        """Create a MatPlotLibOptions instance.

        To ensure accuracy in graph rendering, the default width, height, and DPI should be set with
        the width and height being exact multiples of the DPI. This is because the underlying
        rendering engine uses DPI to determine the pixel dimensions of the output graph from the
        specified width and height in inches.

        If the width and height are not exact multiples of the DPI, it may lead to
        unexpected scaling or distortion of the graph when rendered, as the rendering engine
        may round the pixel dimensions to the nearest whole number.

        The default values provided here are chosen to balance quality and performance for
        most common use cases. However, users can customize these values based on their specific
        requirements for graph resolution and size.

        The use of None for (or, equivalently the omission of) any argument indicates that the default
        value defined in the next lower precedence level should be used.

        Args:
            width (int | None, default=None): The width in pixels of a MatPlotLib output when rendered.
                    It should be an exact multiple of the dpi and can only be between 500 and 4000 pixels.
                    If None, the default MatPlotLibOptions default width will be used.

            height (int | None, default=None): The height in pixels of a MatPlotLib output when rendered.
                    It should be an exact multiple of the dpi and can only be between 500 and 4000 pixels.
                    If None, the default MatPlotLibOptions default height will be used.

            dpi (int | None, default=None): The default DPI (dots per inch) for a MatPlotLib output. It must
                    be between 50 and 400.

            y_starts_at_zero (bool | None, default=None): Whether the Y-axis should start at zero.

            x_labels_rotation (float | None, default=None): The rotation angle in degrees for X-axis labels.

            style (Style | None, default=None): The default style for the MatPlotLib graphs.

            theme (Theme | None, default=None): The theme to use for the MatPlotLib graphs.

            image_type (ImageType | None, default=None): The output format for the graph files.

        Raises:
            SimpleBenchTypeError: If any of the arguments are of incorrect type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._width: int | None = None
        if width is not None:
            self._width = validate_int_range(
                    width, 'width',
                    MatPlotLibOptionsErrorTag.INVALID_WIDTH_ARG_TYPE,
                    MatPlotLibOptionsErrorTag.INVALID_WIDTH_ARG_VALUE,
                    min_value=500, max_value=4000)

        self._height: int | None = None
        if height is not None:
            self._height = validate_int_range(
                    height, 'height',
                    MatPlotLibOptionsErrorTag.INVALID_HEIGHT_ARG_TYPE,
                    MatPlotLibOptionsErrorTag.INVALID_HEIGHT_ARG_VALUE,
                    min_value=500, max_value=4000)

        self._dpi: int | None = None if dpi is None else validate_int_range(
                    dpi, 'dpi',
                    MatPlotLibOptionsErrorTag.INVALID_DPI_ARG_TYPE,
                    MatPlotLibOptionsErrorTag.INVALID_DPI_ARG_VALUE,
                    min_value=50, max_value=400)
        """The DPI (dots per inch) of the graph when rendered (private instance attribute)"""

        self._y_starts_at_zero: bool | None = validate_bool(
            y_starts_at_zero, 'y_starts_at_zero',
            MatPlotLibOptionsErrorTag.INVALID_Y_STARTS_AT_ZERO_ARG_TYPE,
            allow_none=True)
        """Whether the Y-axis should start at zero (private instance attribute)"""

        self._x_labels_rotation: float | None = None if x_labels_rotation is None else validate_float(
            x_labels_rotation, 'x_labels_rotation',
            MatPlotLibOptionsErrorTag.INVALID_X_LABELS_ROTATION_ARG_TYPE)
        """Rotation angle in degrees for X-axis labels (private instance attribute)"""

        self._style: Style | None = None if style is None else validate_type(
            style, Style, 'style',
            MatPlotLibOptionsErrorTag.INVALID_STYLE_ARG_TYPE)
        """Style to use for the MatPlotLib graphs (private instance attribute)"""

        self._theme: Theme | None = None if theme is None else validate_type(
            theme, Theme, 'theme',
            MatPlotLibOptionsErrorTag.INVALID_THEME_ARG_TYPE)
        """Theme to use for the MatPlotLib graphs (private instance attribute)"""

        self._image_type: ImageType | None = None if image_type is None else validate_type(
            image_type, ImageType, 'image_type',
            MatPlotLibOptionsErrorTag.INVALID_IMAGE_TYPE_ARG_TYPE)
        """Type of image to use for the output graph files (private instance attribute)"""

    @property
    def width(self) -> int:
        """Return the width in pixels of the graph when rendered.

        Returns:
            int | None: The width of the graph in pixels when rendered.
        """
        return self._width if self._width is not None else self.get_default_width()

    @property
    def height(self) -> int:
        """Return the height in pixels of the graph when rendered.

        Returns:
            int | None: The height of the graph in pixels when rendered.
        """
        return self._height if self._height is not None else self.get_default_height()

    @property
    def dpi(self) -> int:
        """Return the Dots Per Inch (DPI) of the graph when rendered.

        Returns:
            int | None: The default DPI of the graph when rendered.
        """
        return self._dpi if self._dpi is not None else self.get_default_dpi()

    @property
    def y_starts_at_zero(self) -> bool:
        """Return whether the Y-axis should start at zero.

        Returns:
            bool | None: Whether the Y-axis should start at zero.
        """
        return self._y_starts_at_zero if self._y_starts_at_zero is not None else self.get_default_y_starts_at_zero()

    @property
    def x_labels_rotation(self) -> float:
        """Return the rotation angle in degrees for X-axis labels.

        Returns:
            float | None: The rotation angle in degrees for X-axis labels.
        """
        return self._x_labels_rotation if self._x_labels_rotation is not None else self.get_default_x_labels_rotation()

    @property
    def style(self) -> Style:
        """Return the style for the MatPlotLib graphs.

        Returns:
            Style | None: The style for the MatPlotLib graphs.
        """
        return self._style if self._style is not None else self.get_default_style()

    @property
    def theme(self) -> Theme:
        """Return the theme to use for the MatPlotLib graphs.

        Returns:
            Theme | None: The theme to use for the MatPlotLib graphs.
        """
        return self._theme if self._theme is not None else self.get_default_theme()

    @property
    def image_type(self) -> ImageType:
        """Return the output format for the graph files.

        Returns:
            ImageType | None: The output image format for the graph files.
        """
        return self._image_type if self._image_type is not None else self.get_default_image_type()
