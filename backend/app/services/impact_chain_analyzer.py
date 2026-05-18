def build_deep_call_chains(call_relations):

    graph = {}

    node_map = {}

    for relation in call_relations:

        class_name = relation.get("class_name") or "UnknownClass"

        caller_key = (
            class_name,
            relation["caller"]
        )

        callee_key = (
            class_name,
            relation["callee"]
        )

        caller_node = {
            "class_name": class_name,
            "method": relation["caller"]
        }

        callee_node = {
            "class_name": class_name,
            "method": relation["callee"]
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