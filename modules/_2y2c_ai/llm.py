import asyncio
import json
import re
from itertools import cycle

import aiofiles
import discord
from google import genai
from google.genai.types import GenerateContentConfig

from _2y2c.utils import path
from _2y2c.utils.config import Config


class LLm:
    _instance = None

    def __init__(self):

        self.config = Config()

        self.api_key_list = cycle(self.config.gemini.api_keys)

        self.client = genai.Client(
            api_key=next(self.api_key_list)
        )

        self.generator_config = GenerateContentConfig(
            system_instruction=self._load_system_prompt(),
            temperature=self.config.gemini.temperature,
            top_k=self.config.gemini.top_k,
            top_p=self.config.gemini.top_p,
            max_output_tokens=self.config.gemini.max_tokens
        )

        LLm._instance = self

    def _load_system_prompt(self):
        with open(path.join_path("modules","_2y2c_ai","system_prompt.txt"), "r", encoding="utf-8") as f:
            return f.read()

    async def _load_memory(self):
        async with aiofiles.open(path.join_path("modules","_2y2c_ai","memory.json"), "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)

    async def _load_message_history(self,user_id):
        try:
            async with aiofiles.open(path.join_path("database","message_history.json"), "r", encoding="utf-8") as f:
                content = await f.read()
                data = json.loads(content)
                if data is None:
                    return {}
                return data[user_id]
        except Exception as e:
            print(e)
            return {}

    async def _insert_memory(self, memory_content):
        memory_file = path.join_path(
            "modules",
            "_2y2c_ai",
            "memory.json"
        )

        try:
            async with aiofiles.open(
                    memory_file,
                    "r",
                    encoding="utf-8"
            ) as f:
                content = await f.read()

            if content.strip():
                data = json.loads(content)
            else:
                data = []

            if not isinstance(data, list):
                data = []

        except (
                FileNotFoundError,
                json.JSONDecodeError
        ):
            data = []

        data.append(memory_content)

        async with aiofiles.open(
                memory_file,
                "w",
                encoding="utf-8"
        ) as f:
            await f.write(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=2
                )
            )

    def _split_learning_part(self,message_content):
        pattern = r"\[Learning->\{.*?\}\]"
        match = re.search(pattern, message_content, re.DOTALL)

        if match:
            learning_block = match.group(0)

            response_text = re.sub(pattern, "", message_content, flags=re.DOTALL).strip()

            return response_text,learning_block

        return message_content,None

    @classmethod
    async def start_gen(cls,ctx: discord.Message,prompt: str ,reply_ctx: discord.Message =None):
        LLm = cls._instance

        memory = await LLm._load_memory()

        print(prompt)
        print(reply_ctx)


        def _mentions(message):
            text = message.content

            for user in message.mentions:
                user: discord.Member
                text = re.sub(
                    fr"<@!?{user.id}>",
                    user.display_name,
                    text
                )
            return text

        if reply_ctx:

            prompt = _mentions(ctx)
            reply_content = _mentions(reply_ctx)
            prompt = (f"# Nội dung bạn đã học:\n"
                      f"{memory}\n\n"
                      f"# Lịch sử tin nhắn:\n"
                      f"{await LLm._load_message_history(str(ctx.author.id))}"
                      f"\n\n\n"
                      f"Thông tin người dùng: id=({ctx.author.id}) | account_create_date=({ctx.author.created_at})"
                      f"## Nội dung tin nhắn {ctx.author.display_name} đang reply: {reply_content}\n"
                      f"## Nội dung tin nhắn của {ctx.author.display_name}: {prompt}\n")
        else:
            prompt = (f"# Nội dung bạn đã học:\n"
                      f"{memory}\n\n"
                      f"# Lịch sử tin nhắn:\n"
                      f"{await LLm._load_message_history(str(ctx.author.id))}"
                      f"\n\n\n"
                      f"Thông tin người dùng: id=({ctx.author.id}) | account_create_date=({ctx.author.created_at})"
                      f"## Nội dung tin nhắn của {ctx.author.display_name}: {prompt}\n")
        response = LLm.client.models.generate_content(
            model= LLm.config.gemini.model,
            contents= prompt,
            config= LLm.generator_config,
        )

        print(response.text)

        response,learning = LLm._split_learning_part(response.text)

        if learning:
            await LLm._insert_memory(learning)

        return response

    @classmethod
    async def _gen_test(cls,prompt):
        LLm = cls._instance

        response = await asyncio.to_thread(
            LLm.client.models.generate_content,
            model=LLm.config.gemini.model,
            contents=prompt,
            config=LLm.generator_config,
        )

        response, learning = LLm._split_learning_part(response.text)

        if learning:
            LLm._insert_memory(learning)

        return f"response -> {response}", f"learning -> {learning}"


if __name__ == "__main__":

    async def _load_message_history(user_id):
        try:
            async with aiofiles.open(path.join_path("database", "message_history.json"), "r", encoding="utf-8") as f:
                content = await f.read()
                data = json.loads(content)
                if data is None:
                    return {}
                return data[user_id]
        except Exception as e:
            print(e)
            return {}

    print(asyncio.run(_load_message_history("956930472565407816")))
