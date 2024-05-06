from typing import Any, Dict, Optional, Tuple

import aiohttp
from pydantic import BaseModel, Field

from taitriscore.config import CONFIG


class SerpAPIWrapper:
    """Wrapper around SerpAPI.

    To use, you should have the ``google-search-results`` python package installed,
    and the environment variable ``SERPAPI_API_KEY`` set with your API key, or pass
    `serpapi_api_key` as a named parameter to the constructor.
    """

    def __init__(
        self, search_engine=None, params=None, serpapi_api_key=None, aiosession=None
    ):
        self.search_engine = search_engine
        self.params = params or {
            "engine": "google",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
        }
        self.serpapi_api_key = serpapi_api_key or CONFIG.serpapi_api_key
        self.aiosession = aiosession

    async def run(self, query, **kwargs):
        """Run query through SerpAPI and parse result async."""
        return self._process_response(await self.results(query))

    async def results(self, query):
        """Use aiohttp to run query through SerpAPI and return the results async."""

        def construct_url_and_params():
            params = self.get_params(query)
            params["source"] = "python"
            if self.serpapi_api_key:
                params["serp_api_key"] = self.serpapi_api_key
            params["output"] = "json"
            url = "https://serpapi.com/search"
            return url, params

        url, params = construct_url_and_params()
        if not self.aiosession:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, ssl=False) as response:
                    res = await response.json()
        else:
            async with self.aiosession.get(url, params=params, ssl=False) as response:
                res = await response.json()

        return res

    def get_params(self, query):
        """Get parameters for SerpAPI."""
        _params = {
            "api_key": self.serpapi_api_key,
            "q": query,
        }
        params = {**self.params, **_params}
        return params

    @staticmethod
    def _process_response(res):
        """Process response from SerpAPI."""
        # logger.debug(res)
        focus = ["title", "snippet", "link"]
        get_focused = lambda x: {i: j for i, j in x.items() if i in focus}

        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
            "answer_box" in res.keys()
            and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
            "sports_results" in res.keys()
            and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
            "knowledge_graph" in res.keys()
            and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["snippet"]
        else:
            toret = "No good search result found"

        toret_l = []
        if "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret_l += [get_focused(res["answer_box"])]
        if res.get("organic_results"):
            toret_l += [get_focused(i) for i in res.get("organic_results")]

        return str(toret) + "\n" + str(toret_l)
