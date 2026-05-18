from pydantic import BaseModel


class DiffAnalyzeRequest(BaseModel):

    diff_text: str