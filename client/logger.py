import enum

import disnake
from rgbprint import *


class LogLevel(enum.Enum):
    DEBUG    = ("cyan", "[?]")
    INFO     = ("green", "[+]")
    WARN     = ("yellow", "[*]")
    ERROR    = ("red", "[!]")
    CRITICAL = ("red", "[!!!]")


class Logger:
    def __init__(self, client):
        self.client       = client
        self.log_channels = [] # type: list[disnake.TextChannel]

    async def log(self, message: str, /, *, level: LogLevel = LogLevel.INFO):
        """
        |coro|
        log messages with priorities (red) [!] error \n
        :param message: message to log, it can be any type
        :param level: priority for the log. anything above warn gets sent to the log channel
        """
        if not self.log_channels:
            for id_ in self.client.config["channels"]["logging"]:
                channel = self.client.get_channel(id_)
                if channel:
                    self.log_channels.append(channel)

        match level:
            case LogLevel.DEBUG:
                rgbprint(level.value[1], message, color=level.value[0])

            case LogLevel.INFO:
                rgbprint(level.value[1], message, color=level.value[0])

            case LogLevel.WARN:
                rgbprint(level.value[1], message, color=level.value[0])
                for channel in self.log_channels:
                    await channel.send(f"*`WARN`*```{message}```")

            case LogLevel.ERROR:
                rgbprint(level.value[1], message, color=level.value[0])
                for channel in self.log_channels:
                    await channel.send(f"*`ERROR`*```{message}```")

            case LogLevel.CRITICAL:
                rgbprint(level.value[1], message, color=level.value[0])
                for channel in self.log_channels:
                    await channel.send(f"*`CRITICAL`*```{message}```")
