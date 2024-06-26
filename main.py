import asyncio, discord, os
from discord import Intents
from discord.ext import commands


AMIRI_TOKEN = os.environ["AMIRI_TOKEN"]

intents = Intents.all()

client = commands.Bot(command_prefix="!", intents=intents, owner_id=1110526906106904626)


@client.event
async def on_ready() -> None:
    try:
        await client.change_presence(
            activity=discord.Streaming(
                name="/help", url="https://twitch.tv/gothamchess"))
        print(
            f"----- {client.user.display_name} is Online -----\nServers: {len(client.guilds)}\nMembers: {len(client.users)}"
        )

    except Exception as e:
        print(e)


@client.command()
@commands.is_owner()
async def sync(ctx: commands.Context) -> None:
    await ctx.message.delete()

    fmt = await ctx.bot.tree.sync()

    await ctx.send(f"Synced {len(fmt)} commands", delete_after=3)
    return


async def load():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")


async def main():
    await load()
    await client.start(AMIRI_TOKEN)

asyncio.run(main())