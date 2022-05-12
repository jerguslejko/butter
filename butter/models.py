from typing import List
from pydantic import Field, BaseModel


class Program(BaseModel):
    name: str
    command: str
    working_directory: str = Field(..., alias="working-directory")


class Config(BaseModel):
    name: str
    programs: List[Program]
