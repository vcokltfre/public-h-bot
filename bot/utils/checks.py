from discord.ext import commands

from config.config import dev_ids


def is_dev():
    async def check(ctx: commands.Context):
        return ctx.author.id in dev_ids

    return commands.check(check)

def noh():
    async def check(ctx: commands.Context):
        if ctx.guild and ctx.channel.name == "h":
            return False

        return True

    return commands.check(check)