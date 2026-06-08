from app.indexing.symbol_extractor import extract_symbols


def build_pr_context(changed_files):

    pr_classes = []
    pr_methods = []
    pr_annotations = []

    for file in changed_files:

        patch = file.get("patch", "")

        symbols = extract_symbols(
            patch
        )

        pr_classes.extend(
            symbols["classes"]
        )

        pr_methods.extend(
            symbols["methods"]
        )

        pr_annotations.extend(
            symbols["annotations"]
        )

    return {
        "classes": pr_classes,
        "methods": pr_methods,
        "annotations": pr_annotations
    }