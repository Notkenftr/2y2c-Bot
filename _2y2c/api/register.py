from _2y2c.api.types import CommandTrigger
from _2y2c.modules.command_listeners import CommandListeners as cml
class Register:
    def __init__(self):
        self.command_trigger: CommandTrigger = None
        self.prefix: str = None
        self.command_name = None
        self.set_callback = None


    def register(self):
        if self.command_trigger == CommandTrigger.ON_PREFIX_COMMAND:
            cml.add_to_cm(CommandTrigger.ON_PREFIX_COMMAND,self.callback,cm_name=self.command_name)
        elif self.command_trigger == CommandTrigger.ON_MENTION:
            cml.add_to_cm(CommandTrigger.ON_MENTION,self.callback)