"""KWArgs code generator CLI.

Usage:
    python -m kwargs module.functionname
    python -m kwargs module.ClassName

Generates a KWArgs subclass stub for the specified callable or class.

It is a 'best effort' generator and may require manual adjustments.

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

        def render_arg(arg: Any) -> str:
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


def generate_kwargs_class(callable_obj: Any, class_name: str, func_name: str) -> str:
    """Generate a KWArgs subclass for the given callable or class."""
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
    init_body: str = f'        super().__init__({class_name}.{func_name}, kwargs=locals(), globalns=globals())'

    class_doc = f'KWArgs for {class_name}.{func_name}'
    init_doc = callable_doc or f'Initialize KWArgs for {class_name}.{func_name}.'

    # Compose the import section, including type_imports
    import_lines = [
        f'from {callable_obj.__module__} import {class_name}',
        'from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE',
    ]
    import_lines.extend(type_imports)
    import_section = '\n'.join(sorted(import_lines))

    kwargs_class_name = _kwargs_class_name(class_name, func_name)
    init_doc_lines = init_doc.split('\n')
    if len(init_doc_lines) > 1:
        init_doc = init_doc_lines[0] + '\n\n' + '\n'.join(f'        {line}' for line in init_doc_lines[1:])
    code = f'''"""KWArgs subclass for {class_name}.{func_name}."""

{import_section}

class {kwargs_class_name}(KWArgs):
    """{class_doc}"""

    def __init__(self, *,
{init_params}) -> None:
        """{init_doc}"""
{init_body}
'''
    return code

def _kwargs_class_name(class_name: str, func_name: str) -> str:
    """Generate a KWArgs class name based on the class and function names.

    :param class_name: The name of the class.
    :type class_name: str
    :param func_name: The name of the function or method.
    :type func_name: str
    :return: A string representing the KWArgs class name.
    """
    if func_name == '__init__':
        return f'{class_name}KWArgs'
    func_elements = func_name.split('_')
    func_elements = [elem.capitalize() for elem in func_elements]
    func_part = ''.join(func_elements)
    return f'{class_name}{func_part}KWArgs'


def _is_function_name(name: str) -> bool:
    if not name:
        return False
    if name.startswith('__') and name.endswith('__') and len(name) > 4:
        return True
    if name[0].isupper():
        return False
    if name[0] == '_' and len(name) > 1 and name[1].islower():
        return True
    return False

def _is_class_name(name: str) -> bool:
    if not name:
        return False
    if name.startswith('__') and name.endswith('__') and len(name) > 4:
        return False
    if name[0].isupper():
        return True
    if name[0] == '_' and len(name) > 1 and name[1].isupper():
        return True
    return False

def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python -m kwargs module.callable')
        sys.exit(1)
    target = sys.argv[1]
    if '.' not in target:
        print('Error: Specify as module.callable')
        sys.exit(1)

    module_name, attr_name = target.rsplit('.', 1)

    if _is_class_name(attr_name):
        class_name = attr_name
        func_name = '__init__'

    elif _is_function_name(attr_name):
        module_name, class_name, func_name = target.rsplit('.', 2)

    else:
        print('Error: Could not determine if target is a class or function. '
              'Ensure the name follows Python naming conventions.')
        sys.exit(1)


    # print(f'# Generating KWArgs for {module_name}.{class_name}.{func_name}...')
    try:
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        callable_obj = getattr(cls, func_name)
    except ImportError as exc:
        print(f'Error: Could not import module "{module_name}": {exc}')
        sys.exit(1)
    except AttributeError:
        print(f'Error: Module "{module_name}" has no attribute "{attr_name}"')
        sys.exit(1)
    code = generate_kwargs_class(callable_obj, class_name, func_name)
    print(code)


if __name__ == '__main__':
    main()
