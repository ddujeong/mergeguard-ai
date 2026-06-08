from collections import Counter

from app.repository.models import CodeSymbol


def build_repo_context(
        repository_id,
        db
):

    symbols = db.query(
        CodeSymbol
    ).filter(
        CodeSymbol.repository_id == repository_id
    ).all()

    annotation_counter = Counter()

    class_names = []

    for symbol in symbols:

        if symbol.annotation:
            annotation_counter[
                symbol.annotation
            ] += 1

        if symbol.class_name:
            class_names.append(
                symbol.class_name
            )

    controllers = len([
        c for c in class_names
        if "Controller" in c
    ])

    services = len([
        c for c in class_names
        if "Service" in c
    ])

    response_classes = [
        c for c in class_names
        if "Response" in c
        or "ApiResponse" in c
    ]

    security_classes = [
        c for c in class_names
        if (
            "Security" in c
            or "Jwt" in c
            or "UserDetails" in c
        )
    ]

    return {
        "controllers": controllers,
        "services": services,
        "common_annotations":
            annotation_counter.most_common(10),
        "response_classes":
            response_classes,
        "security_classes":
            security_classes
    }