from pydantic import BaseModel


class RepoIndexRequest(BaseModel):

    owner: str

    repo: str