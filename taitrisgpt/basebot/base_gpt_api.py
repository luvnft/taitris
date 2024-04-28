from abc import abstractmethod
from typing import Optional

from taitrisgpt.logs import logger
from taitrisgpt.basebot.base_chatbot import BaseChatbot


class BaseGPTAPI(BaseChatbot):
    def __init__(self):
        self.system_prompt = "You are a helpful assistant."

    def _user_msg(self, msg):
        return {"role": "user", "content": msg}

    def _assistant_msg(self, msg):
        return {"role": "assistant", "content": msg}

    def _system_msg(self, msg):
        return {"role": "system", "content": msg}

    def _system_msgs(self, msgs):
        return [self._system_msg(msg) for msg in msgs]

    def _default_system_msg(self):
        return self._system_msg(self.system_prompt)

    def ask(self, msg):
        message = [self._default_system_msg(), self._user_msg(msg)]
        rsp = self.completion(message)
        return self.get_choice_text(rsp)

    async def aask(self, msg, system_msgs=None):
        if system_msgs:
            message = self._system_msgs(system_msgs) + [self._user_msg(msg)]
        else:
            message = [self._default_system_msg(), self._user_msg(msg)]
        rsp = await self.acompletion_text(message, stream=True)
        logger.debug(message)
        # logger.debug(rsp)
        return rsp

    def _extract_assistant_rsp(self, context):
        return "\n".join([i["content"] for i in context if i["role"] == "assistant"])

    def ask_batch(self, msgs):
        context = []
        for msg in msgs:
            umsg = self._user_msg(msg)
            context.append(umsg)
            rsp = self.completion(context)
            rsp_text = self.get_choice_text(rsp)
            context.append(self._assistant_msg(rsp_text))
        return self._extract_assistant_rsp(context)

    async def aask_batch(self, msgs):
        """Sequential questioning"""
        context = []
        for msg in msgs:
            umsg = self._user_msg(msg)
            context.append(umsg)
            rsp_text = await self.acompletion_text(context)
            context.append(self._assistant_msg(rsp_text))
        return self._extract_assistant_rsp(context)
