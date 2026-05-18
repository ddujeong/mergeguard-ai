def build_deep_call_chains(call_relations):

    graph = {}

    for relation in call_relations:

        caller = relation["caller"]
        callee = relation["callee"]

        if caller not in graph:
            graph[caller] = []

        graph[caller].append(callee)

    visited = set()

    chains = []

    def dfs(method, path, depth):

        if depth > 4:
            return

        if method in visited:
            return

        visited.add(method)

        next_calls = graph.get(method, [])

        if not next_calls:

            chains.append(path.copy())

        for next_method in next_calls:

            path.append(next_method)

            dfs(
                next_method,
                path,
                depth + 1
            )

            path.pop()

    for start_method in graph.keys():

        visited.clear()

        dfs(
            start_method,
            [start_method],
            0
        )

    return chains