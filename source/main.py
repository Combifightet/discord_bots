import discord
from discord.ext import commands
import os

BOT_TOKEN:str = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
	latency = round(bot.latency, 2)
	print(f'Latency is `{latency}ms`')
	await ctx.send(f'Latency is {latency}ms')


def main():
	bot.run(BOT_TOKEN)

if __name__ == '__main__':
	main()
