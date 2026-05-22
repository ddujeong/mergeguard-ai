import re


CLASS_PATTERN = r"class\s+(\w+)"

METHOD_PATTERN = r"(public|private|protected)\s+[\w<>]+\s+(\w+)\s*\("

ANNOTATION_PATTERN = r"@(\w+)"

INTERFACE_PATTERN = r"implements\s+(\w+)"

def extract_symbols(content: str):

    classes = re.findall(
        CLASS_PATTERN,
        content
    )

    methods = re.findall(
        METHOD_PATTERN,
        content
    )

    annotations = re.findall(
        ANNOTATION_PATTERN,
        content
    )

    interfaces = re.findall(
        INTERFACE_PATTERN,
        content
    )

    return {
        "classes": classes,
        "methods": [m[1] for m in methods],
        "annotations": annotations,
        "interfaces": interfaces
    }