from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseChatbot(ABC):
    """Abstract GPT class"""

    mode = "API"

    @abstractmethod
    def ask(self, msg):
        """Ask GPT a question and get an answer"""

    @abstractmethod
    def ask_batch(self, msgs):
        """Ask GPT multiple questions and get a series of answers"""
