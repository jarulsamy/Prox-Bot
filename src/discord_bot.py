import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
from pyproxmoxer.proxmox import Proxmox


def check_channel(ctx):
    return str(ctx.channel) == CHANNEL


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(check_channel)
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"Hello {member}")

    @commands.command()
    @commands.check(check_channel)
    async def kill(self, ctx):
        await ctx.send(f"Stopping upon the request of {ctx.author.mention}")
        await self.bot.close()
        exit(0)

    @commands.command()
    @commands.check(check_channel)
    async def stop(self, ctx):
        await ctx.send(f"Stopping upon the request of {ctx.author.mention}")
        await self.bot.close()
        exit(0)


class ProxCommands(commands.Cog):
    def __init__(self, bot, prox):
        self.bot = bot
        self.prox = prox

    @commands.command()
    @commands.check(check_channel)
    async def server(self, ctx):
        for i in self.prox.get_vms():
            if i.running:
                await (ctx.send(f"{i.name} ({i.id}) is alreading running."))
            else:
                await ctx.send(f"{i.name} ({i.id}) is not running, starting...")
                self.prox.start_vms()

    @commands.command()
    @commands.check(check_channel)
    async def status(self, ctx):
        for i in self.prox.get_vms():
            await ctx.send(
                f"{i.name} ({i.id}) => {'Running' if i.running else 'Stopped'}"
            )


if __name__ == "__main__":
    load_dotenv()

    BOT_PREFIX = "?"
    TOKEN = os.getenv("TOKEN")
    CHANNEL = "proxmox"

    prox = Proxmox(
        os.getenv("PROX_USER"),
        os.getenv("PROX_PASS"),
        os.getenv("PROX_HOST"),
        os.getenv("PROX_NODE_NAME"),
    )

    vms = prox.get_vms()
    if not len(vms):
        print("No VMs defined, quitting...")
        exit(-1)

    bot = Bot(command_prefix=BOT_PREFIX)
    bot.add_cog(GeneralCommands(bot))
    bot.add_cog(ProxCommands(bot, prox))

    bot.run(TOKEN)
