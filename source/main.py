import discord
from discord.ext import commands
import os

# from cogs import embed

BOT_TOKEN:str = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")

	for filename in os.listdir('source/cogs'):
		if filename.endswith('.py'):
			await bot.load_extension(f'cogs.{filename[:-3]}')
	
	# Sync all app commands
	try:
		synced = await bot.tree.sync()
		print(f'Synced {len(synced)} application commands')
		print(synced)
	except Exception as e:
		print(f"Error syncing commands: {e}")


# Manual sync command for testing
@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
	await ctx.message.delete()
	try:
		synced = await ctx.bot.tree.sync(guild=None)
		print(f"Synced {len(synced)} command(s)")
	except Exception as e:
		print(f"Failed to sync: {e}")



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
