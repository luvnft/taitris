# from taitriscore.basebot.anthropic_api import AnthropicAPI as LLM
# from taitriscore.basebot.hf_api import LLAMAV2API as LLM
from taitriscore.basebot.openai_api import OpenAIGPTAPI as LLM

DEFAULT_LLM = LLM()


async def ai_func(prompt):
    return await DEFAULT_LLM.aask(prompt)
