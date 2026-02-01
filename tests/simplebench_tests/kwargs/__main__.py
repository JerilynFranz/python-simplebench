"""KWArgs code generator CLI.

Usage:
    python -m kwargs module.functionname
    python -m kwargs module.ClassName

Generates a KWArgs subclass for the specified callable or class.
"""

import importlib
import inspect
import sys
import types
import typing
from typing import Any, get_args, get_origin


def get_type_name(t: Any) -> str:
    origin = get_origin(t)
    args = get_args(t)

    # Handle new union syntax (A | B) in Python 3.10+ and typing.Union
    if origin is typing.Union or isinstance(t, types.UnionType):
        return ' | '.join(get_type_name(arg) for arg in args)

    if origin:
        if origin in (list, dict, set, tuple):
            name = origin.__name__
        elif hasattr(origin, '__qualname__'):
            name = origin.__qualname__
        else:
            name = str(origin)

        def render_arg(arg):
            if isinstance(arg, (tuple, list)):
                return '[' + ', '.join(get_type_name(a) for a in arg) + ']' if arg else '[]'
            return get_type_name(arg)

        args_str = ', '.join(render_arg(arg) for arg in args)
        return f'{name}[{args_str}]'
    elif t is type(None):
        return 'NoDefaultValue'
    elif hasattr(t, '__qualname__'):
        return t.__qualname__
    elif hasattr(t, '__name__'):
        return t.__name__
    else:
        return str(t)


def get_type_imports(params: list[inspect.Parameter]) -> set[str]:
    imports = set()

    def collect(t: Any) -> None:
        origin = get_origin(t)
        args = get_args(t)
        # Handle new union syntax (A | B) in Python 3.10+ and typing.Union
        if origin is typing.Union or isinstance(t, types.UnionType):
            for arg in args:
                collect(arg)
            return
        # Recursively collect imports for generics and their arguments
        if args:
            for arg in args:
                collect(arg)
        if t is type(None) or getattr(t, '__module__', None) == 'builtins':
            return
        if hasattr(t, '__qualname__') and hasattr(t, '__module__'):
            top_level = t.__qualname__.split('.')[0]
            imports.add(f'from {t.__module__} import {top_level}')

    for p in params:
        ann = p.annotation
        collect(ann)

    return imports


def generate_kwargs_class(callable_obj: Any, name: str) -> str:
    """Generate a KWArgs subclass for the given callable or class."""
    if inspect.isclass(callable_obj):
        sig = inspect.signature(callable_obj.__init__)
        callable_doc = inspect.getdoc(callable_obj.__init__)
    else:
        sig = inspect.signature(callable_obj)
        callable_doc = inspect.getdoc(callable_obj)
    params = [p for p in sig.parameters.values() if p.name != 'self']

    # Collect imports for parameter types
    type_imports = get_type_imports(params)

    # Build parameter lines with modern | type hints and NoDefaultValue
    init_param_lines: list[str] = []
    for p in params:
        ann = p.annotation
        annotation_str = get_type_name(ann)
        # Always add NoDefaultValue to the type hint if not already present
        if 'NoDefaultValue' not in annotation_str.split(' | '):
            annotation_str = f'{annotation_str} | NoDefaultValue'
        default = 'NO_DEFAULT_VALUE'
        param_line = f'            {p.name}: {annotation_str} = {default}'
        init_param_lines.append(param_line)

    init_params = ',\n'.join(init_param_lines)
    init_body = '        super().__init__({k: v for k, v in locals().items() if k != "self"})'
    class_doc = f'KWArgs for {name}'
    init_doc = callable_doc or f'Initialize KWArgs for {name}.'

    # Compose the import section, including type_imports
    import_lines = [
        f'from {callable_obj.__module__} import {name}',
        'from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE',
    ]
    import_lines.extend(type_imports)
    import_section = '\n'.join(sorted(import_lines))

    init_doc_lines = init_doc.split('\n')
    if len(init_doc_lines) > 1:
        init_doc = init_doc_lines[0] + '\n\n' + '\n'.join(f'        {line}' for line in init_doc_lines[1:])
    code = f'''"""KWArgs subclass for {name}."""

{import_section}

class {name}KWArgs(KWArgs):
    """{class_doc}"""

    def __init__(self, *,
{init_params}) -> None:
        """{init_doc}"""
{init_body}
'''
    return code

def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python -m kwargs module.callable')
        sys.exit(1)
    target = sys.argv[1]
    if '.' not in target:
        print('Error: Specify as module.callable')
        sys.exit(1)
    module_name, attr_name = target.rsplit('.', 1)
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        print(f'Error: Could not import module "{module_name}": {exc}')
        sys.exit(1)
    try:
        callable_obj = getattr(module, attr_name)
    except AttributeError:
        print(f'Error: Module "{module_name}" has no attribute "{attr_name}"')
        sys.exit(1)
    code = generate_kwargs_class(callable_obj, attr_name)
    print(code)

if __name__ == '__main__':
    main()
