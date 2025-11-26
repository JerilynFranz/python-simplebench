"""Options for the scatter plot reporter"""
from simplebench.reporters.graph.matplotlib import MatPlotLibOptions


class ScatterPlotOptions(MatPlotLibOptions):
    """Scatter Plot options.

    Defaults are inherited from :class:`~.MatPlotLibOptions`:

    * ``width: int = 1500``
    * ``height: int = 750``
    * ``dpi: int = 150``
    * ``y_starts_at_zero: bool = True``
    * ``x_labels_rotation: float = 45.0``
    * ``style: Style = Style.DARK_BACKGROUND``
    * ``theme: Theme = Theme.Default``
    * ``image_type: ImageType = ImageType.SVG``
    """
