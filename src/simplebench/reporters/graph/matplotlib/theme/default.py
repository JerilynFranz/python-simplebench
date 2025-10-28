"""Default theme for Matplotlib graphs."""
from .base import Theme as BaseTheme


DefaultTheme = BaseTheme({
        'axes.grid': True,
        'grid.linestyle': '-',
        'grid.color': '#444444',
        'legend.framealpha': 1,
        'legend.shadow': True,
        'legend.fontsize': 14,
        'legend.title_fontsize': 16,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'axes.labelsize': 16,
        'axes.titlesize': 20,
        'figure.dpi': 150
    })
"""Default Matplotlib graph theme."""
