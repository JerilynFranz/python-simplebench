"""Tests for the reporter.graph.matplotlib Themes."""
import pytest

from simplebench.reporters.graph.matplotlib.theme import DefaultTheme, Theme


@pytest.mark.parametrize("theme", [
        pytest.param(DefaultTheme, id="DEFAULT_001 - DefaultTheme"),
])
def test_preset_themes(theme: Theme) -> None:
    """Test Theme class initialization."""
    assert isinstance(theme, Theme), f"Theme is not an instance of Theme: {type(theme)}"
