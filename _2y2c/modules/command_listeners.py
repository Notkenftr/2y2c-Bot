import json

import aiofiles
import discord
from discord.ext import commands

from _2y2c.api.types import CommandTrigger
from _2y2c.utils import path

class CommandListeners(commands.Cog):

    _instance = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        CommandListeners._instance = self
        self.command_map = {}
        self.on_mention_command = []

    async def on_prefix_trigger(self,message):
        if message.author.bot:
            return
        if message.author.id == self.bot.user.id:
            return
        parts = message.content.split(" ", 1)

        command_name = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if command_name in self.command_map:
            func = self.command_map[command_name]
            await func(message,args)
    async def on_mention_trigger(self,message,reply_ctx=None):
        if message.author.bot:
            return

        args = message.content

        for command in self.on_mention_command:
            await command(message,reply_ctx,args)
    async def _insert_chat_history(self, message):
        file_path = path.join_path(
            "database",
            "message_history.json"
        )

        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                data = json.loads(content) if content.strip() else {}
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if not isinstance(data, dict):
            data = {}

        msg_text = f"{message.author.name}: {message.content}"

        author_id = str(message.author.id)
        data.setdefault(author_id, [])
        data[author_id].append(msg_text)

        for user in message.mentions:
            uid = str(user.id)
            data.setdefault(uid, [])
            data[uid].append(msg_text)

        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=2
                )
            )
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return
        await self._insert_chat_history(message)
        if message.author.id == self.bot.user.id:
            return

        try:

            if message.reference:

                original = await message.channel.fetch_message(
                    message.reference.message_id
                )

                if original.author.id == self.bot.user.id:
                    await self.on_mention_trigger(message,original)

        except discord.NotFound:
            pass


        if message.content.startswith(f"<@{self.bot.user.id}>"):
            await self.on_mention_trigger(message,None)
        else:
            await self.on_prefix_trigger(message)

        async def write():
            with open(path.join_path("database","message_old.log"),'a',encoding='utf-8') as f:
                f.write(f"{message.author.name}: {message.content}\n")

        await write()
    @classmethod
    def add_to_cm(cls,cm_type,callback,cm_name = ""):

        if cm_type == CommandTrigger.ON_PREFIX_COMMAND:
            if cm_name == "":
                print("Cần set command name")
                return
            cls._instance.command_map[f"!{cm_name}"] = callback
        elif cm_type == CommandTrigger.ON_MENTION:
            cls._instance.on_mention_command.append(callback)
        print(cls._instance.on_mention_command)
        print(cls._instance.command_map)