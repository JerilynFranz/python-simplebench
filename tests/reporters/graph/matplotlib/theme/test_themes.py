"""Tests for the reporter.graph.matplotlib Themes."""
import pytest

from simplebench.reporters.graph.matplotlib.theme import Theme, DefaultTheme


@pytest.mark.parametrize("theme", [
        pytest.param(DefaultTheme, id="DEFAULT_001 - DefaultTheme"),
])
def test_preset_themes(theme):
    """Test Theme class initialization."""
    assert isinstance(theme, Theme), f"Theme is not an instance of Theme: {type(theme)}"
