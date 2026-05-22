from sqlalchemy.orm import Session

from app.github.repo_fetcher import fetch_repo_tree
from app.indexing.hash_service import calculate_file_hash

from app.repository.models import Repository
from app.repository.models import RepoFileIndex


def index_repository(
        owner: str,
        repo: str,
        db: Session
):

    java_files = fetch_repo_tree(
        owner,
        repo
    )

    repository_entity = Repository(
        owner=owner,
        name=repo
    )

    db.add(repository_entity)

    db.commit()

    db.refresh(repository_entity)

    indexed_files = []

    for file in java_files:

        file_hash = calculate_file_hash(
            file["content"]
        )

        file_index = RepoFileIndex(
            repository_id=repository_entity.id,
            path=file["path"],
            content_hash=file_hash,
            language="java"
        )

        db.add(file_index)

        indexed_files.append({
            "path": file["path"],
            "hash": file_hash,
            "preview": file["content"][:200]
        })

    db.commit()

    return {
        "owner": owner,
        "repo": repo,
        "file_count": len(java_files),
        "files": indexed_files[:5]
    }