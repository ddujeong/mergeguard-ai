from sqlalchemy.orm import Session

from app.github.repo_fetcher import fetch_repo_tree
from app.indexing.hash_service import calculate_file_hash

from app.repository.models import Repository
from app.repository.models import RepoFileIndex
from app.indexing.symbol_extractor import extract_symbols
from app.repository.models import CodeSymbol

def index_repository(
        owner: str,
        repo: str,
        db: Session
):

    java_files = fetch_repo_tree(
        owner,
        repo
    )

    repository_entity = db.query(
        Repository
    ).filter(
        Repository.owner == owner,
        Repository.name == repo
    ).first()


    if not repository_entity:

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
        symbols = extract_symbols(
            file["content"]
        )

        existing_file = db.query(
            RepoFileIndex
        ).filter(
            RepoFileIndex.repository_id == repository_entity.id,
            RepoFileIndex.path == file["path"]
        ).first()

        if existing_file:

            if existing_file.content_hash == file_hash:

                print(f"skip : {file['path']}")

                indexed_files.append({
                    "path": file["path"],
                    "hash": file_hash,
                    "status": "SKIPPED",
                    "preview": file["content"][:200]
                })

                continue

            existing_file.content_hash = file_hash

            status = "UPDATED"

            print(f"updated : {file['path']}")

        else:

            file_index = RepoFileIndex(
                repository_id=repository_entity.id,
                path=file["path"],
                content_hash=file_hash,
                language="java"
            )

            db.add(file_index)

            status = "INSERTED"

            print(f"inserted : {file['path']}")

        # 기존 symbol 삭제 후 재저장
        db.query(CodeSymbol).filter(
            CodeSymbol.repository_id == repository_entity.id,
            CodeSymbol.file_path == file["path"]
        ).delete()

        for class_name in symbols["classes"]:
            db.add(CodeSymbol(
                repository_id=repository_entity.id,
                file_path=file["path"],
                symbol_type="CLASS",
                class_name=class_name
            ))

        for method_name in symbols["methods"]:
            db.add(CodeSymbol(
                repository_id=repository_entity.id,
                file_path=file["path"],
                symbol_type="METHOD",
                method_name=method_name
            ))

        for annotation in symbols["annotations"]:
            db.add(CodeSymbol(
                repository_id=repository_entity.id,
                file_path=file["path"],
                symbol_type="ANNOTATION",
                annotation=annotation
            ))

        for interface in symbols["interfaces"]:
            db.add(CodeSymbol(
                repository_id=repository_entity.id,
                file_path=file["path"],
                symbol_type="INTERFACE",
                interface=interface
            ))
        
        indexed_files.append({
            "path": file["path"],
            "hash": file_hash,
            "status": status,
            "symbols": symbols,
            "preview": file["content"][:200]
        })

    db.commit()

    return {
        "owner": owner,
        "repo": repo,
        "file_count": len(java_files),
        "files": indexed_files[:5]
    }