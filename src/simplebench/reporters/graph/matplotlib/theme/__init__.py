"""Themes for Matplotlib graphs.

It consists of the base Theme class and instances of defined themes.

Custom themes can be created either by creating Theme instances directly or
by using the .replace() method of existing Theme instances to override specific rcParams.
"""
from simplebench.reporters.graph.matplotlib.theme.exceptions import ThemeErrorTag
from simplebench.reporters.graph.matplotlib.theme.base import Theme
from simplebench.reporters.graph.matplotlib.theme.default import DefaultTheme

__all__ = [
    'ThemeErrorTag',
    'Theme',
    'DefaultTheme',
]
"""Themes for Matplotlib graphs."""
