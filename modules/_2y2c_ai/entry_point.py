import random

import discord
from _2y2c.api.register import Register
from _2y2c.api.types import CommandTrigger
from _2y2c.utils.config import Config
from _2y2c.utils import path
from google import genai
from google.genai.types import GenerateContentConfig

from modules._2y2c_ai.llm import LLm

class EntryPoint(Register):
    def __init__(self):
        super().__init__()
        self.command_trigger = CommandTrigger.ON_MENTION
        self.set_callback = self.callback
        self.register()

    def load_system_prompt(self):
        with open(path.join_path("modules","_2y2c_ai","system_prompt.txt"), "r", encoding="utf-8") as f:
            return f.read()

    def load_history(self, limit=125):
        with open(
                path.join_path("database", "message_old.log"),
                "r",
                encoding="utf-8"
        ) as f:
            lines = f.readlines()

        return "".join(lines[-limit:])



    async def callback(self,ctx: discord.Message,reply_ctx: discord.Message,arg):
        llm = LLm()

        try:
            response = await llm.start_gen(ctx=ctx,prompt=arg,reply_ctx=reply_ctx)
            await ctx.reply(response)
        except:
            import traceback
            traceback.print_exc()
            await ctx.reply("Hết mẹ token rồi^^")

