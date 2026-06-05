from discord.ext import commands

from _2y2c.loader import Loader
from _2y2c.modules.command_listeners import CommandListeners
from _2y2c.utils.config import Config
from discord.ext import commands

from _2y2c.loader import Loader
from _2y2c.modules.command_listeners import CommandListeners
from _2y2c.utils.config import Config


class App(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            self_bot=True
        )
        self.config = Config()
        self.cml = CommandListeners(self)

    def dispatch(self, event_name, /, *args, **kwargs):

        if event_name == "message":
            message = args[0]

            cfg = self.config.discord

            if (
                    cfg.is_only_guild
                    and (
                    message.guild is None
                    or message.guild.id not in cfg.only_guild_ids
            )
            ):
                return

        return super().dispatch(
            event_name,
            *args,
            **kwargs
        )


    async def on_ready(self):
        print(f"Đã login vào {self.user.name}")
        print(f"Đang load cogs...")
        await self.add_cog(CommandListeners(self))
        print(f"Đã load xong CmL")
        print("Load modules")
        loader = Loader(self.cml,self)
        loader.load_all()
        print("Done.")

    def _start(self):
        self.run(self.config.discord.token)

if __name__ == "__main__":
    bot = App()
    bot._start()
