import os
import yaml
from _2y2c.utils import path
from types import SimpleNamespace

class Config:
    def __init__(self):
        self.config_data = self._load_config_data()

        self.discord = SimpleNamespace()
        self.discord_obj = self.config_data.get("Discord", {})

        self.discord.token = self.discord_obj.get("token")
        self.discord.is_only_guild = (
            self.discord_obj.get("only_guild", {})
            .get("enable", False)
        )
        self.discord.only_guild_ids = (
            self.discord_obj.get("only_guild", {})
            .get("ids", [])
        )

        self.gemini = SimpleNamespace()
        self.gemini_obj = self.config_data.get("Gemini", {})

        self.gemini.api_keys = self.gemini_obj.get("api_key", [])

        self.gemini.model = self.gemini_obj.get(
            "model",
            "gemini-3.1-flash-lite"
        )

        self.gemini.temperature = self.gemini_obj.get(
            "temperature",
            0.7
        )

        self.gemini.top_p = self.gemini_obj.get(
            "top_p",
            0.9
        )

        self.gemini.top_k = self.gemini_obj.get(
            "top_k",
            50
        )

        self.gemini.max_tokens = self.gemini_obj.get(
            "max_tokens",
            8192
        )
    def _load_config_data(self):
        config_path = path.join_path("config.yml")

        if not os.path.exists(config_path):
            raise FileNotFoundError(config_path)

        with open(config_path,'r',encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config

