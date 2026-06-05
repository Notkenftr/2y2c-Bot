from enum import Enum

class CommandTrigger(Enum):
    ON_PREFIX_COMMAND = "ON_PREFIX_COMMAND"
    ON_MENTION = "ON_MENTION"
    ON_CUSTOM_TRIGGER = "ON_CUSTOM_TRIGGER"