import pdb

from pydantic import BaseModel, Field

from taitriscore.config import CONFIG
from taitriscore.environment import Environment
from taitriscore.logs import logger
from taitriscore.roles import Role
from taitriscore.utils.schema import Message

class Campaign(BaseModel):
    environment: Environment = Field(default_factory=Environment)
    company: str = Field(default="")
    objective: str = Field(default="")

    def hire(self, roles):
        self.environment.add_roles(roles=roles)

    def set_quota_seeding(self, quota_seeding):
        CONFIG.max_quota_seeding = quota_seeding
        logger.info(f"Quota Seeding: {quota_seeding}.")

    def budget(self, budget):
        CONFIG.max_budget = budget
        logger.info(f"Budget: ${budget}.")

    def _check_balance(self):
        if CONFIG.total_seeding > CONFIG.max_quota_seeding:
            raise f"No More products to place -> Nb of Products placed: {CONFIG.total_seedings}"

    def start_campaign(self, objective):
        self.objective = objective

    async def run(self, n_round=3):
        while n_round > 0:
            n_round -= 1
            logger.debug(f"{n_round}")
            self._check_balance()
            await self.environment.run()
        return self.environment.history
