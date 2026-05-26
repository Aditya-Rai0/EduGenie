from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class AgentInput(BaseModel):
    job_id: str
    course_id: str
    data: dict[str, Any]


class AgentOutput(BaseModel):
    job_id: str
    status: str
    result: dict[str, Any]
    metadata: dict[str, Any] = {}


class BaseAgent(ABC):

    def __init__(self, name: str, model: str = "gpt-4o"):
        self.name = name
        self.model = model

    @abstractmethod
    async def run(self, input_data: AgentInput) -> AgentOutput:
        ...
