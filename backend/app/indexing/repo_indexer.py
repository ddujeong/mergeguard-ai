from app.github.repo_fetcher import fetch_repo_tree
from app.indexing.hash_service import calculate_file_hash


def index_repository(owner: str, repo: str):

    java_files = fetch_repo_tree(
        owner,
        repo
    )

    indexed_files = []

    for file in java_files:

        file_hash = calculate_file_hash(
            file["content"]
        )

        indexed_files.append({
            "path": file["path"],
            "hash": file_hash,
            "preview": file["content"][:200]
        })

    return {
        "owner": owner,
        "repo": repo,
        "file_count": len(java_files),
        "files": indexed_files[:5]
    }