"""Enums used in the simplebench.reporters.graph package."""
from enum import Enum
from simplebench.enums import enum_docstrings


@enum_docstrings
class Style(str, Enum):
    """Enumeration of graph styles.

    The styles correspond to those available in Matplotlib 3.10.6
    """
    BMH = "bmh"
    """Bayesian Methods for Hackers style for graphs.
    https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/
    """
    CLASSIC = "classic"
    """Light background style for graphs.

    Classic matplotlib plotting style
    """
    DARK_BACKGROUND = "dark_background"
    """Dark background style for graphs.

    Set black background default line colors to white.
    """
    FIVETHIRTYEIGHT = "fivethirtyeight"
    """FiveThirtyEight style for graphs.

    Replicated styles from FiveThirtyEight.com
    See https://www.dataorigami.net/blogs/fivethirtyeight-mpl
    """
    GGPLOT = "ggplot"
    """ggplot style for graphs.

    Replicates the style of R's ggplot library.
    See https://everyhue.me/posts/sane-color-scheme-for-matplotlib/
    """
    GRAYSCALE = "grayscale"
    """Grayscale style for graphs.

    Set all colors to grayscale
    Note: strings of float values are interpreted by matplotlib as gray values.
    """
    PETTROF10 = "petroff10"
    """Petroff10 style for graphs.

    Color cycle survey palette from Petroff (2021):
    https://arxiv.org/abs/2107.02270
    https://github.com/mpetroff/accessible-color-cycles
    """
    SEABORN_V0_8 = "seaborn-v0_8"
    """Base Seaborn style for graphs."""
    SEABORN_V0_8_BRIGHT = "seaborn-v0_8-bright"
    """Seaborn bright style for graphs."""
    SEABORN_V0_8_COLORBLIND = "seaborn-v0_8-colorblind"
    """Seaborn colorblind style for graphs."""
    SEABORN_V0_8_DARK = "seaborn-v0_8-dark"
    """Seaborn dark style for graphs."""
    SEABORN_V0_8_DARK_PALETTE = "seaborn-v0_8-dark-palette"
    """Seaborn dark palette style for graphs."""
    SEABORN_V0_8_DARKGRID = "seaborn-v0_8-darkgrid"
    """Seaborn darkgrid style for graphs."""
    SEABORN_V0_8_DEEP = "seaborn-v0_8-deep"
    """Seaborn deep style for graphs."""
    SEABORN_V0_8_MUTED = "seaborn-v0_8-muted"
    """Seaborn muted style for graphs."""
    SEABORN_V0_8_NOTEBOOK = "seaborn-v0_8-notebook"
    """Seaborn notebook style for graphs."""
    SEABORN_V0_8_PAPER = "seaborn-v0_8-paper"
    """Seaborn paper style for graphs."""
    SEABORN_V0_8_PASTEL = "seaborn-v0_8-pastel"
    """Seaborn pastel style for graphs."""
    SEABORN_V0_8_POSTER = "seaborn-v0_8-poster"
    """Seaborn poster style for graphs."""
    SEABORN_V0_8_TALK = "seaborn-v0_8-talk"
    """Seaborn talk style for graphs."""
    SEABORN_V0_8_TICKS = "seaborn-v0_8-ticks"
    """Seaborn ticks style for graphs."""
    SEABORN_V0_8_WHITE = "seaborn-v0_8-white"
    """Seaborn white style for graphs."""
    SEABORN_V0_8_WHITEGRID = "seaborn-v0_8-whitegrid"
    """Seaborn whitegrid style for graphs."""
    SOLARIZE_LIGHT2 = "Solarize_Light2"
    """Solarized light style for graphs.

    Solarized color palette taken from https://ethanschoonover.com/solarized/
    """
    TABLEAU_COLORBLIND10 = "tableau-colorblind10"
    """Tableau colorblind10 style for graphs."""
