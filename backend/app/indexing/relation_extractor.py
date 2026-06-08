def extract_relations(ast_result):

    relations = []

    for relation in ast_result["call_relations"]:

        relations.append({
            "caller_class":
                relation["caller_class"],

            "caller_method":
                relation["caller"],

            "callee_class":
                relation["callee_class"],

            "callee_method":
                relation["callee"],

            "relation_type":
                "METHOD_CALL"
        })

    return relations