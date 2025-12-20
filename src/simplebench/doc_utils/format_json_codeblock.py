"""Utility for formatting JSON data into an RST code-block for docstrings."""
from json import JSONEncoder
from textwrap import dedent, indent


def format_json_for_docstring(
        json_data: dict[str, object] | str,
        caption: str,
        intro_text: str) -> str:
    """Generate a reStructuredText (RST) formatted string containing a JSON code-block.

    This utility is designed to embed pretty-printed JSON data directly into
    Python docstrings in a way that Sphinx can correctly render as a
    `code-block` directive.

    :param json_data: The JSON data to format. Can be a dictionary (which will
                      be pretty-printed) or a pre-formatted string.
    :type json_data: dict[str, object] | str
    :param caption: The caption to use for the `code-block` directive.
    :type caption: str
    :param intro_text: A line of introductory text to place before the code block.
    :type intro_text: str
    :return: A string containing the formatted RST code-block.
    :rtype: str
    """
    # 1. Ensure we have a pretty-printed JSON string if a dict is passed.
    if isinstance(json_data, dict):
        json_text = JSONEncoder(indent=2).encode(json_data)
    else:
        json_text = json_data

    # 2. Define a clean, dedented template for the note.
    # The placeholder {schema_text} is where the indented JSON will go.
    template = dedent("""
        {intro}

        .. code-block:: json
           :caption: {caption}

        {schema_text}
        """)

    # 3. Indent the JSON text to align with the code-block directive's content area.
    # A standard 3-space indent is conventional for directives.
    indented_json_text = indent(json_text, "   ")

    # 4. Format the template to create the final RST block.
    return template.format(
        intro=intro_text,
        caption=caption,
        schema_text=indented_json_text
    )
