"""Helper for unpacking and validating forward references in type hints"""
import inspect
from typing import Any, ForwardRef, get_args, get_origin, get_type_hints


def resolve_type_hint(type_hint: Any,
                      globalns: dict[str, Any] | None = None,
                      localns: dict[str, Any] | None = None,
                      depth: int = 100) -> Any:
    """Resolve a type hint, recursively resolving any ForwardRef within generic arguments.

    
    :param Any type_hint: The type hint to resolve.
    :param dict[str, Any] | None globalns: The global namespace for evaluation.
    :param dict[str, Any] | None localns: The local namespace for evaluation.
    :param int depth: (default=100) Maximum recursion depth to prevent infinite loops.
        Type hints will be resolved up to this depth. This is intended to prevent infinite recursion
        in the case of circular references or pathological cases. If depth reaches zero, the type hint
        is returned as-is without further resolution.
    :return Any: The resolved type.
    """
    if depth <= 0:
        return type_hint
    # Infer globalns from type_hint if possible, else from caller if not provided
    frame: Any = None  # Reused frame variable for both globalns and localns efficiency
    if globalns is None:
        globalns = getattr(type_hint, '__globals__', None)
        if globalns is None:
            frame = inspect.currentframe()
            if frame is not None:
                caller = frame.f_back
                if caller is not None:
                    globalns = caller.f_globals

    # Infer localns from caller if not provided
    if localns is None:
        frame = frame or inspect.currentframe()
        if frame is not None:
            caller = frame.f_back
            if caller is not None:
                localns = caller.f_locals

    # Recursively resolve ForwardRef
    if isinstance(type_hint, ForwardRef):
        try:
            resolved = get_type_hints(type_hint, globalns=globalns, localns=localns).get(type_hint.__forward_arg__, Any)
        except (NameError, AttributeError, ImportError):
            return type_hint
        return resolve_type_hint(resolved, globalns, localns, depth - 1)

    # Recursively resolve generic arguments
    origin = get_origin(type_hint)
    args = get_args(type_hint)
    if origin and args:
        resolved_args = tuple(resolve_type_hint(arg, globalns, localns, depth - 1) for arg in args)
        try:
            return origin[resolved_args]
        except TypeError:
            # Some built-in generics may not support subscription with resolved_args
            return type_hint

    return type_hint

__all__ = [
    "resolve_type_hint",
]
