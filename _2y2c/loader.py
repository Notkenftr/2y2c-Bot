import importlib
import os

from discord.ext import commands

from _2y2c.modules.command_listeners import CommandListeners
from _2y2c.utils import path


class Loader:
    def __init__(self,cml: CommandListeners,app: commands.Bot):
        self.cmd = cml
        self.app = app

    def load_all(self):
        modules_path = path.join_path("modules")

        for module in os.listdir(modules_path):
            module_path = os.path.join(modules_path,module)
            if not os.path.isdir(module_path):
                continue

            entry_point = os.path.join(module_path,"entry_point.py")
            _spec = importlib.util.spec_from_file_location("entry_point",entry_point)
            module = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(module)

            ep = module.EntryPoint
            ep()
