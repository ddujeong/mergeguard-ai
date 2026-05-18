from tree_sitter import Language, Parser
from tree_sitter_java import language


JAVA_LANGUAGE = Language(language())

parser = Parser(JAVA_LANGUAGE)


def extract_java_structure(code: str):

    tree = parser.parse(
        bytes(code, "utf-8")
    )

    root = tree.root_node

    classes = []

    methods = []

    method_calls = []

    stack = [root]

    while stack:

        node = stack.pop()

        if node.type == "class_declaration":

            name_node = node.child_by_field_name("name")

            if name_node:

                classes.append(
                    name_node.text.decode("utf-8")
                )

        if node.type == "method_declaration":

            name_node = node.child_by_field_name("name")

            if name_node:

                methods.append(
                    name_node.text.decode("utf-8")
                )
        if node.type == "method_invocation":

            name_node = node.child_by_field_name("name")

            if name_node:
                method_calls.append(
                    name_node.text.decode("utf-8")
                )
        stack.extend(node.children)

    return {
        "classes": list(set(classes)),
        "methods": list(set(methods)),
        "method_calls": list(set(method_calls))
    }


def analyze_changed_structure(files: list):

    all_classes = []

    all_methods = []

    all_method_calls = []
    
    for file in files:

        filename = file.get("filename", "")

        if not filename.endswith(".java"):
            continue

        patch = file.get("patch", "")

        if not patch:
            continue

        result = extract_java_structure(patch)

        all_classes.extend(
            result["classes"]
        )

        all_methods.extend(
            result["methods"]
        )
        
        all_method_calls.extend(
            result["method_calls"]
        )

    return {
        "classes": list(set(all_classes)),
        "methods": list(set(all_methods)),
        "method_calls": list(set(all_method_calls))
    }