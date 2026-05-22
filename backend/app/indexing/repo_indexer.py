from app.github.repo_fetcher import fetch_repo_tree


def index_repository(owner: str, repo: str):

    java_files = fetch_repo_tree(
        owner,
        repo
    )

    print(f"indexed files : {len(java_files)}")

    return {
        "owner": owner,
        "repo": repo,
        "file_count": len(java_files),
        "files": [
            {
                "path": file["path"],
                "preview": file["content"][:200]
            }
            for file in java_files[:5]
        ]
    }