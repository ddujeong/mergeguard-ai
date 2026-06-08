import re


FIELD_PATTERN = (
    r"private\s+final\s+(\w+)\s+(\w+);"
)


def extract_dependencies(content: str):

    matches = re.findall(
        FIELD_PATTERN,
        content
    )

    dependency_map = {}

    for class_name, variable_name in matches:

        dependency_map[
            variable_name
        ] = class_name

    return dependency_map