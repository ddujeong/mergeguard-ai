def build_call_chains(call_relations):

    graph = {}

    for relation in call_relations:

        caller = relation["caller"]
        callee = relation["callee"]

        if caller not in graph:
            graph[caller] = []

        graph[caller].append(callee)

    chains = []

    visited = set()

    def dfs(node, path):

        if node in visited:
            return

        visited.add(node)

        path.append(node)

        if node not in graph:

            chains.append(path[:])

        else:

            for next_node in graph[node]:

                dfs(next_node, path[:])

    for caller in graph.keys():

        dfs(caller, [])

    return chains