from app.repository.models import SymbolRelation


def find_impacted_classes(
        repository_id,
        changed_class,
        db
):

    impacted = set()

    queue = [changed_class]

    while queue:

        current = queue.pop(0)

        relations = db.query(
            SymbolRelation
        ).filter(
            SymbolRelation.repository_id == repository_id,
            SymbolRelation.callee_class == current
        ).all()

        for relation in relations:

            caller = relation.caller_class

            if caller not in impacted:

                impacted.add(caller)

                queue.append(caller)

    return list(impacted)