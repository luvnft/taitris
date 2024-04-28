import asyncio
import fire

from taitrisgpt.memory.memory import Memory
from taitrisgpt.logs import logger
from taitrisgpt.roles import Planner

import pdb


async def create_plan(objective: str):
    
    role = Planner(profile="Planner", objective = objective)
    
    final_list = await role.generate_tasks_list(objective)
    logger.info(final_list)
    

def main(objective):
    # Wrap the asyncio call in a synchronous function
    return asyncio.run(create_plan(objective))

if __name__ == "__main__":
    fire.Fire(main)


# OBJECTIVE = """You are hired to lead an influencers marketing campaign for Taitris, a company selling innovative candles smelling like wood.
#     You have access to instagram.
#     Find the right influencers, reach out and try to do product seeding to bring some new clients to Taitris."""