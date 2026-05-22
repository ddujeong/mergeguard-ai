from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.repository.db import Base


class Repository(Base):

    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)

    owner = Column(String, nullable=False)

    name = Column(String, nullable=False)

    default_branch = Column(String, default="main")

    indexed_at = Column(DateTime(timezone=True),
                        server_default=func.now())


class RepoFileIndex(Base):

    __tablename__ = "repo_file_indexes"

    id = Column(Integer, primary_key=True, index=True)

    repository_id = Column(Integer, nullable=False)

    path = Column(String, nullable=False)

    content_hash = Column(String, nullable=False)

    language = Column(String)

    indexed_at = Column(DateTime(timezone=True),
                        server_default=func.now())