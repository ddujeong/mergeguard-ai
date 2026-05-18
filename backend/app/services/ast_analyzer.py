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

    call_relations = []

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

            method_name_node = node.child_by_field_name("name")

            if method_name_node:

                method_name = (
                    method_name_node.text.decode("utf-8")
                )

                methods.append(method_name)

                body_node = node.child_by_field_name("body")

                if body_node:

                    body_stack = [body_node]

                    while body_stack:

                        body_child = body_stack.pop()

                        if body_child.type == "method_invocation":

                            call_name_node = (
                                body_child.child_by_field_name("name")
                            )

                            if call_name_node:

                                called_method = (
                                    call_name_node.text.decode("utf-8")
                                )

                                method_calls.append(
                                    called_method
                                )

                                call_relations.append({
                                    "caller": method_name,
                                    "callee": called_method
                                })

                        body_stack.extend(
                            body_child.children
                        )

        stack.extend(node.children)

    return {
        "classes": list(set(classes)),
        "methods": list(set(methods)),
        "method_calls": list(set(method_calls)),
        "call_relations": call_relations
    }


def analyze_changed_structure(files: list):

    all_classes = []

    all_methods = []

    all_method_calls = []
    all_call_relations = []
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

        all_call_relations.extend(
            result["call_relations"]
        )
    
    unique_call_relations = []

    seen = set()

    for relation in all_call_relations:

        key = (
            relation["caller"],
            relation["callee"]
        )

        if key not in seen:

            seen.add(key)

            unique_call_relations.append(relation)

    return {
        "classes": list(set(all_classes)),
        "methods": list(set(all_methods)),
        "method_calls": list(set(all_method_calls)),
        "call_relations": unique_call_relations
    }