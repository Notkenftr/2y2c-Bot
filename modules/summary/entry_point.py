import random

import discord
from _2y2c.api.register import Register
from _2y2c.api.types import CommandTrigger
from _2y2c.utils.config import Config
from _2y2c.utils import path
from google import genai
from google.genai.types import GenerateContentConfig

class EntryPoint(Register):
    def __init__(self):
        super().__init__()
        self.command_trigger = CommandTrigger.ON_PREFIX_COMMAND
        self.command_name = "summary"
        self.set_callback = self.callback
        self.register()

    def load_system_prompt(self):
        with open(path.join_path("modules","summary","system_prompt.txt"), "r", encoding="utf-8") as f:
            return f.read()

    def load_history(self, limit=125):
        with open(
                path.join_path("database", "message_old.log"),
                "r",
                encoding="utf-8"
        ) as f:
            lines = f.readlines()

        return "".join(lines[-limit:])
    async def callback(self,ctx: discord.Message,arg):
        print("trigger summary")
        prompt = (f"Lịch sử tin nhắn:\n {self.load_history()}\n\n Hết lịch sử\n\n")
        config = Config()

        client = genai.Client(
            api_key=random.choice(config.gemini.api_keys),
        )

        genai_config = GenerateContentConfig(
            system_instruction=self.load_system_prompt(),
            temperature=config.gemini.temperature,
            top_k=config.gemini.top_k,
            top_p=config.gemini.top_p,
            max_output_tokens=config.gemini.max_tokens,
        )
        try:
            response = client.models.generate_content(
                model = config.gemini.model,
                config=genai_config,
                contents=prompt
            )
        except:
            await ctx.reply("Hết mẹ token rồi^^")

        await ctx.reply(response.text)
