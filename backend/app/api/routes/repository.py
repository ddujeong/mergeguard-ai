from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.repository.db import get_db
from app.analysis.ripple_graph_analyzer import (
    find_impacted_classes
)

router = APIRouter(
    prefix="/api/v1/repositories",
    tags=["Repository"]
)


@router.get("/{repository_id}/ripple")
def analyze_ripple(
        repository_id: int,
        changed_class: str,
        db: Session = Depends(get_db)
):

    impacted_classes = (
        find_impacted_classes(
            repository_id=repository_id,
            changed_class=changed_class,
            db=db
        )
    )

    return {
        "changed_class": changed_class,
        "impacted_classes": impacted_classes,
        "impact_count": len(
            impacted_classes
        )
    }