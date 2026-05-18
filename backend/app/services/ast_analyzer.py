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
    current_class = None
    variable_types = {}

    stack = [root]

    while stack:

        node = stack.pop()
        if node.type == "local_variable_declaration":

            type_node = node.child_by_field_name("type")

            declarator_node = None

            for child in node.children:

                if child.type == "variable_declarator":
                    declarator_node = child
                    break

            if type_node and declarator_node:

                variable_name_node = (
                    declarator_node.child_by_field_name("name")
                )

                if variable_name_node:

                    variable_name = (
                        variable_name_node.text.decode("utf-8")
                    )

                    variable_type = (
                        type_node.text.decode("utf-8")
                    )

                    variable_types[variable_name] = variable_type
        if node.type == "class_declaration":
            
            name_node = node.child_by_field_name("name")

            if name_node:
                current_class = (
                    name_node.text.decode("utf-8")
                )
                classes.append(current_class)

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

                            object_node = (
                                body_child.child_by_field_name("object")
                            )

                            if call_name_node:

                                called_method = (
                                    call_name_node.text.decode("utf-8")
                                )

                                object_name = None
                                
                                object_class = None

                                if object_node:
                                    object_name = (
                                        object_node.text.decode("utf-8")
                                    )
                                    object_class = variable_types.get(object_name)

                                method_calls.append(called_method)

                                call_relations.append({
                                    "class_name": current_class,
                                    "caller": method_name,
                                    "callee": called_method,
                                    "object_name": object_name,
                                    "object_class": object_class
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
            relation["class_name"],
            relation["caller"],
            relation["callee"],
            relation.get("object_name")
        )

        if key not in seen:

            seen.add(key)

            unique_call_relations.append(relation)
    defined_methods = set(all_methods)
    called_methods = set(all_method_calls)

    undefined_calls = []

    for call in called_methods:
        if call not in defined_methods:
            undefined_calls.append(call)
    sensitive_keywords = [
        "login",
        "logout",
        "auth",
        "token",
        "jwt",
        "password",
        "credential",
        "delete",
        "payment",
        "admin",
        "extract",
        "userid",
        "validate"
    ]

    sensitive_methods = []

    for method in set(all_methods + all_method_calls):
        lower_method = method.lower()

        for keyword in sensitive_keywords:
            if keyword in lower_method:
                sensitive_methods.append(method)
                break
    high_keywords = [
        "login",
        "logout",
        "token",
        "jwt",
        "password",
        "credential",
        "delete",
        "payment",
        "admin"
    ]

    medium_keywords = [
        "auth",
        "extract",
        "userid",
        "validate",
        "check",
        "verify"
    ]

    method_risks = []

    for method in set(all_methods + all_method_calls):

        lower_method = method.lower()

        risk_level = "LOW"

        for keyword in high_keywords:

            if keyword in lower_method:
                risk_level = "HIGH"
                break

        if risk_level != "HIGH":

            for keyword in medium_keywords:

                if keyword in lower_method:
                    risk_level = "MEDIUM"
                    break

        method_risks.append({
            "method": method,
            "risk_level": risk_level
        })
    return {
        "classes": list(set(all_classes)),
        "methods": list(set(all_methods)),
        "method_calls": list(set(all_method_calls)),
        "call_relations": unique_call_relations,
        "undefined_calls": undefined_calls,
        "sensitive_methods": sensitive_methods,
        "method_risks": method_risks
    }