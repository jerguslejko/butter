from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class Program(BaseModel):
    name: str
    command: str
    working_directory: str = Field(..., alias="working-directory")
    env: Dict[str, str] = Field(default_factory=dict)


class Command(BaseModel):
    name: str
    command: str
    mode: Optional[Literal["downtime", "instant"]] = "instant"
    working_directory: str = Field(..., alias="working-directory")


class Config(BaseModel):
    name: str
    path: str
    programs: List[Program]
    commands: Optional[List[Command]]
