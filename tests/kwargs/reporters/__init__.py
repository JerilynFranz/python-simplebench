"""KWArgs package fortests of simplebench.reporters classes."""
from .choice_conf_kwargs import ChoiceConfKWArgs
from .choice_kwargs import ChoiceKWArgs
from .choices_conf_kwargs import ChoicesConfKWArgs
from .choices_kwargs import ChoicesKWArgs
from .reporter import (
    DispatchToTargetsMethodKWArgs,
    RenderByCaseMethodKWArgs,
    RenderBySectionMethodKWArgs,
    ReporterKWArgs,
)

__all__ = [
    'ChoiceKWArgs',
    'ChoiceConfKWArgs',
    'ChoicesKWArgs',
    'ChoicesConfKWArgs',
    'DispatchToTargetsMethodKWArgs',
    'ReporterKWArgs',
    'RenderByCaseMethodKWArgs',
    'RenderBySectionMethodKWArgs',
]
