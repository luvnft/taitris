# from taitrisgpt.basebot.anthropic_api import Claude2 as Claude
# from taitrisgpt.basebot.hf_api import LLAMAV2API as LLM
from taitrisgpt.basebot.openai_api import OpenAIGPTAPI as LLM

DEFAULT_LLM = LLM()


async def ai_func(prompt):
    return await DEFAULT_LLM.aask(prompt)
