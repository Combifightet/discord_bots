import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
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
			# Formatting: https://www.pythondiscord.com/pages/guides/python-guides/discord-messages-with-colors/
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
				ephemeral = True # only for debuggin final version sould send an actual message
			)
	

async def setup(bot):
	await bot.add_cog(Duden(bot))



# ---------------------- Parsing Util ---------------------- #

class Meaning:
	def __init__(self, meaning:str|None, infos:dict[str, tuple[str, str|None]]|None, examples:list[str]):
		"""
		Class that holds a meaning object, only used for structuring data
		Args:
			meaning (str): The meaning text
			tuples (dict[str, tuple[str, str | None]] | None): A dict of additional information about the meaning<br>dict(\<title\>, tuple(\<content\>, \<link\>))
			examples (list[str]): A list of example sentences for this meaning
		"""
		self.meaning = meaning
		self.infos = infos
		self.examples = examples
	
	def __str__(self):
		infoString:str = ''
		if self.infos:
			for info in self.infos.keys():
				infoString += f'\n  {info}: {self.infos[info][0]}'
				if self.infos[info][1] is not None:
					infoString += f' ({self.infos[info][1]})'

		examplesString:str = ''
		if self.examples:
			examplesString = '\n  Examples:'
			for example in self.examples:
				examplesString += f'\n   - {example}'

		return f'{self.meaning}\n{infoString}\n{examplesString}'
	

def tuplesToDict(tuples:ResultSet) -> dict[str, tuple[str, str|None]]:
	result:dict[str, str] = {}
	for tuple in tuples:
		linkTag:Tag = tuple.find('dd').find('a')
		link:str = None
		if linkTag is not None:
			link = linkTag.get('href')

		result[tuple.find('dt').text] = (tuple.find('dd').text.lstrip('\n').rstrip('\n'), link)
	return result

def dictValWhereKeyContains(d:dict[str, tuple[str, str|None]], keyPart:str, caseSensitive=False) -> str | None:
	for k in d.keys():
		if (caseSensitive and keyPart in k) or (not caseSensitive and keyPart.lower() in k.lower()):
			return d[k]
	return None

def generateMeaningsField(meanings:list[Meaning]):
	pass
