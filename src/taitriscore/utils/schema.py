from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel
from typing_extensions import Type, TypedDict

from taitriscore.logs import logger


class RawMessage(TypedDict):
    content: str
    role: str


@dataclass
class Message:
    content: str
    instruct_content: BaseModel = field(default=None)
    role: str = field(default="user")  # system / user / assistant
    cause_by: Type["Action"] = field(default="")
    sent_from: str = field(default="")
    send_to: str = field(default="")

    def __str__(self):
        return f"{self.role}: {self.content}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {"role": self.role, "content": self.content}


@dataclass
class UserMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, "user")


@dataclass
class SystemMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, "system")


@dataclass
class AIMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, "assistant")


if __name__ == "__main__":
    test_content = "test_message"
    msgs = [
        UserMessage(test_content),
        SystemMessage(test_content),
        AIMessage(test_content),
        Message(test_content, role="QA"),
    ]
    logger.info(msgs)
