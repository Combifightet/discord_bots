import discord
import os

BOT_TOKEN:str = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'Bot Logged in as {client.user}')

def main():
	client.run(BOT_TOKEN)

if __name__ == '__main__':
	main()