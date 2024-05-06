import asyncio
import pdb
from typing import Iterable

from pydantic import BaseModel, Field

from taitriscore.memory import Memory
from taitriscore.roles import Role
from taitriscore.utils.schema import Message


class Environment(BaseModel):
    roles: dict = Field(default_factory=dict)
    memory: Memory = Field(default_factory=Memory)
    history: str = Field(default="")

    class Config:
        arbitrary_types_allowed = True

    def add_role(self, role):
        role.set_env(self)
        self.roles[role.profile] = role

    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)

    def publish_message(self, message):
        self.memory.add(message)
        self.history += f"\n{message}"

    async def run(self, k=1):
        for _ in range(k):
            futures = []
            for role in self.roles.values():
                future = role.run()
                futures.append(future)
            await asyncio.gather(*futures)

    def get_roles(self):
        return self.roles

    def get_role(self, name):
        return self.roles.get(name, None)
