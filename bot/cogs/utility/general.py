import time
import discord
from discord.ext import commands

from bot.bot import Bot
from bot.utils.checks import is_dev
from config.config import name


class General(commands.Cog):
    """A general purpose cog for tasks such as cog loading"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(name="cogs")
    @is_dev()
    async def cogs_group(self, ctx: commands.Context):
        """Perform actions such as reloading cogs"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Usage: `!cogs <load | reload | unload> [list of cogs]`")

    @cogs_group.command(name="load")
    async def load_cogs(self, ctx: commands.Context, *cognames):
        """Load a set of cogs"""
        log = ""
        for cog in cognames:
            cog = "bot.cogs." + cog
            try:
                self.bot.load_extension(cog)
                log += f"Successfully loaded cog {cog}\n"
            except Exception as e:
                log += f"Failed to load cog {cog}: {e}\n"
                self.bot.logger.error(f"Cog loading: failed to load {cog}: {e}")

        self.bot.logger.info(f"Loaded cog(s):\n{log}")
        await ctx.send(log)

    @cogs_group.command(name="reload")
    async def reload_cogs(self, ctx: commands.Context, *cognames):
        """Reload a set of cogs"""
        log = ""
        for cog in cognames:
            cog = "bot.cogs." + cog
            try:
                self.bot.reload_extension(cog)
                log += f"Successfully reloaded cog {cog}\n"
            except Exception as e:
                log += f"Failed to reload cog {cog}: {e}\n"
                self.bot.logger.error(f"Cog reloading: failed to reload {cog}: {e}")

        self.bot.logger.info(f"Reloaded cog(s):\n{log}")
        await ctx.send(log)

    @cogs_group.command(name="unload")
    async def unload_cogs(self, ctx: commands.Context, *cognames):
        """Unload a set of cogs - you cannot unload utility.general"""
        log = ""
        for cog in cognames:
            cog = "bot.cogs." + cog
            try:
                if cog == "bot.cogs.utility.general":
                    raise Exception("You cannot unload this cog!")
                self.bot.unload_extension(cog)
                log += f"Successfully unloaded cog {cog}\n"
            except Exception as e:
                log += f"Failed to unload cog {cog}: {e}\n"
                self.bot.logger.error(f"Cog unloading: failed to unload {cog}: {e}")

        self.bot.logger.info(f"Unloaded cog(s):\n{log}")
        await ctx.send(log)

    @commands.command(name="restart", aliases=["reboot", "shutdown"])
    @is_dev()
    async def restart(self, ctx: commands.Context):
        """Make the bot logout"""
        await ctx.send("Restarting...")
        self.bot.logger.info(f"Shutting down {name}")
        await self.bot.close()

    @commands.command(name="ping")
    @is_dev()
    async def ping(self, ctx: commands.Context):
        t_start = time.time()
        m = await ctx.channel.send("Testing RTT for message editing.")
        await m.edit(content="Testing...")
        rtt = time.time() - t_start
        await m.edit(
            content=f"Pong!\nMessage edit RTT: {round(rtt * 1000, 2)}ms\nWebsocket Latency: {round(self.bot.latency * 1000, 2)}ms")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name="https://letterh.xyz"))
        self.bot.logger.info(f"{name} has started")


def setup(bot: Bot):
    bot.add_cog(General(bot))
