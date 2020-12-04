import discord
from discord.ext import commands
from discord.utils import get

from bot.bot import Bot
from bot.utils.checks import noh


class EnsureH(commands.Cog):
    """Only. h."""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def guild_setup(self, guild: discord.Guild):
        if not get(guild.channels, name="h"):
            self.bot.logger.info(f"Setting up guild {guild.id}...")
            channel = await guild.create_text_channel(name="h", reason="Setting up h environment...")
            inv = await channel.create_invite(max_age=0, max_uses=0, reason=f"Setting up h environment...")
            await channel.send("No h channel was found so one was created for you. Thank you for using h Bot!\n\n*(All messages after this will be h enforced)*")
            self.bot.logger.info(f"Successfully set up guild {guild.id}, invite: {inv.url}")

    @commands.command(name="invite", aliases=["inv"])
    @noh()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def invite(self, ctx: commands.Context):
        invite = f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=93201&scope=bot"
        embed = discord.Embed(title="Invite h Bot", description=f"[Invite Me]({invite})", colour=0x87CEEB)
        embed.set_footer(text="h Bot by vcokltfre#6868")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.webhook_id or not message.guild:
            return

        if message.channel.name == "h" and not message.content == "h":
            await message.delete()
            await message.author.send("h. Only h. Nothing but h. Comprende?")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        channel = self.bot.get_channel(payload.channel_id)

        if channel.name == "h":
            message = await channel.fetch_message(payload.message_id)
            await message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.guild_setup(guild)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.guild_setup(guild)


def setup(bot: Bot):
    bot.add_cog(EnsureH(bot))
