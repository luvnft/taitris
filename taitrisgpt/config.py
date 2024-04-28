import os

import abc

from dotenv import load_dotenv
import yaml

from taitrisgpt.const import PROJECT_ROOT
from taitrisgpt.logs import logger
from taitrisgpt.tools import SearchEngineType, WebBrowserEngineType

import pdb


# Load .env file
dotenv_path = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=dotenv_path)


class Singleton(abc.ABCMeta, type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NotConfiguredException(Exception):
    def __init__(self, message="The required configuration is not set"):
        self.message = message
        super().__init__(self.message)


class Config(metaclass=Singleton):
    _instance = None
    key_yaml_file = PROJECT_ROOT / "taitrisgpt/config/key.yaml"
    default_yaml_file = PROJECT_ROOT / "taitrisgpt/config/config.yaml"

    def __init__(self, yaml_file=default_yaml_file):
        self._configs = {}
        self._init_with_config_files_and_env(self._configs, yaml_file)
        logger.info("Config loading done.")
        self.max_tokens_rsp = self._get("MAX_TOKENS", 2048)
        # self.claude_api_key = self._get('Anthropic_API_KEY')
        self.serpapi_api_key = self._get("SERPAPI_API_KEY")
        self.openai_api_key = self._get("OPENAI_API_KEY")
        self.openai_api_base = self._get("OPENAI_API_BASE")
        self.openai_model = self._get("OPENAI_MODEL")
        self.HUGGINGFACE_API_KEY = self._get("HUGGINGFACE_API_KEY")
        self.llama_model_name = self._get("LLAMA_MODEL_NAME")
        self.search_engine = self._get("SEARCH_ENGINE", SearchEngineType.SERPAPI_GOOGLE)
        self.web_browser_engine = WebBrowserEngineType(
            self._get("WEB_BROWSER_ENGINE", WebBrowserEngineType.PLAYWRIGHT)
        )
        self.selenium_browser_type = self._get("SELENIUM_BROWSER_TYPE", "chrome")
        self.long_term_memory = self._get("LONG_TERM_MEMORY", False)
        if self.long_term_memory:
            logger.warning("LONG_TERM_MEMORY is True")
        self.max_budget = self._get("MAX_BUDGET", 10.0)
        self.max_quota_seeding = self._get("MAX_QUOTA_SEEDING", 10)
        self.total_seeding = 0
        self.total_cost = 0.0
        self.update_costs = self._get("UPDATE_COSTS", True)
        self.calc_usage = self._get("CALC_USAGE", True)
        self.rpm = self._get("RPM", 10)
        self.model_for_researcher_summary = self._get("MODEL_FOR_RESEARCHER_SUMMARY")
        self.model_for_researcher_report = self._get("MODEL_FOR_RESEARCHER_REPORT")

    def _init_with_config_files_and_env(self, configs: dict, yaml_file):
        configs.update(os.environ)

        for _yaml_file in [yaml_file, self.default_yaml_file]:
            if not _yaml_file.exists():
                continue

            with open(_yaml_file, "r", encoding="utf-8") as file:
                yaml_data = yaml.safe_load(file)
                if not yaml_data:
                    continue
                os.environ.update(
                    {k: v for k, v in yaml_data.items() if isinstance(v, str)}
                )
                configs.update(yaml_data)

    def _get(self, key, default=None):
        return self._configs.get(key, default)

    def get(self, key, *args, **kwargs):
        value = self._get(key, *args, **kwargs)
        if value is None:
            raise ValueError(
                f"Key '{key}' not found in environment variables or in the YAML file"
            )
        return value


CONFIG = Config()
