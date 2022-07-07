from typing import Dict, List
from pydantic import Field, BaseModel


class Program(BaseModel):
    name: str
    command: str
    working_directory: str = Field(..., alias="working-directory")
    env: Dict[str, str] = Field(default_factory=dict)


class Config(BaseModel):
    name: str
    path: str
    programs: List[Program]
