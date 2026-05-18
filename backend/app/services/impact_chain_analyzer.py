def build_deep_call_chains(call_relations):

    graph = {}

    node_map = {}

    for relation in call_relations:

        caller_key = (
            relation.get("caller_class") or "UnknownClass",
            relation["caller"]
        )

        callee_key = (
            relation.get("callee_class") or "UnknownClass",
            relation["callee"]
        )

        caller_node = {
            "class_name": caller_key[0],
            "method": caller_key[1]
        }

        callee_node = {
            "class_name": callee_key[0],
            "method": callee_key[1]
        }

        node_map[caller_key] = caller_node
        node_map[callee_key] = callee_node

        if caller_key not in graph:
            graph[caller_key] = []

        graph[caller_key].append(callee_key)

    chains = []

    def dfs(method_key, path, visited, depth):

        if depth > 4:
            return

        if method_key in visited:
            return

        visited.add(method_key)

        next_calls = graph.get(method_key, [])

        if not next_calls:
            chains.append([
                node_map[key]
                for key in path
            ])
            return

        for next_key in next_calls:

            dfs(
                next_key,
                path + [next_key],
                visited.copy(),
                depth + 1
            )

    for start_key in graph.keys():

        dfs(
            start_key,
            [start_key],
            set(),
            0
        )

    return chains

def calculate_ripple_effect(chains):

    max_depth = 0

    visited_methods = set()
    security_methods = set()

    security_keywords = [
        "auth",
        "token",
        "password",
        "login",
        "jwt"
    ]

    for chain in chains:

        max_depth = max(
            max_depth,
            len(chain)
        )

        for node in chain:

            method_key = (
                node["class_name"],
                node["method"]
            )

            visited_methods.add(method_key)

            method_text = (
                f"{node['class_name']}.{node['method']}"
                .lower()
            )

            if any(
                keyword in method_text
                for keyword in security_keywords
            ):
                security_methods.add(method_key)

    total_calls = len(visited_methods)
    security_count = len(security_methods)

    score = (
        total_calls * 8
        + max_depth * 10
        + security_count * 12
    )

    if score >= 120:
        level = "HIGH"

    elif score >= 60:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "score": score,
        "level": level,
        "max_depth": max_depth,
        "total_affected_methods": total_calls,
        "security_related_calls": security_count
    }