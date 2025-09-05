import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime
from bs4 import BeautifulSoup
import requests


class Duden(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print('Loaded Duden cog')

	@app_commands.command(name = 'duden',description = 'perform a word look up in ther german dictionary \'Duden\'')
	@app_commands.describe(word = 'The word to be looked up')
	async def duden(self, interaction: discord.Interaction, word: str):
		"""Slash command to look up a word in Duden"""

		response: requests.Response = requests.get(f'https://www.duden.de/rechtschreibung/{word}')
		soup = BeautifulSoup(response.text, 'html.parser')

		# print('\n')
		# print(soup.find('meta', property='og:url')['content'])
		# print('\n')

		if (response.status_code>=400 and response.status_code<500):
			print(f'can\'t find a duden entry for \'{word}\'')
			# TODO: implement search
			await interaction.response.send_message(
				f'can\'t find a duden entry for \'{word}\'',
				ephemeral = True
			)
		else:
			embed: discord.Embed = discord.Embed(
				title = soup.find('h1').text,
				url = soup.find('meta', property='og:url')['content'],
				color = 0xf9cf26,
				# description = f'should be for this word: \'{word}\'',
				timestamp = datetime.now()
			)
			embed.set_image(url = soup.find('meta', property='og:image:url')['content'])
			embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Duden_Logo_2017.svg/330px-Duden_Logo_2017.svg.png')

			await interaction.response.send_message(
				embed = embed,
				ephemeral = True
			)
	

async def setup(bot):
	await bot.add_cog(Duden(bot))
