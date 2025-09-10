import discord
from discord.ext import commands
from discord import app_commands


class  Texts(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print('Loaded  Texts cog')

	@app_commands.command(name = 'colors', description = 'display all text and background colors')
	async def colors(self, interaction: discord.Interaction):
		"""Slash command to display all possible text and background colors"""

		embed: discord.Embed = discord.Embed(
			title = 'Text Colors',
			url = 'https://www.pythondiscord.com/pages/guides/python-guides/discord-messages-with-colors/',
			# color = 0xf9cf26,
			description = """
To be able to send a colored text, you need to use the ansi language for your code block and provide a prefix of this format before writing your text:
```
\\u001b[{format};{color}m
```
All possible formats are:
```ansi
 • 0: \u001b[0;00mNormal\u001b[0m
 • 1: \u001b[1;00mBold\u001b[0m
 • 4: \u001b[4;00mUnderline\u001b[0m
```

All possible colors are:
```ansi
\u001b[1;30;40m Text \u001b[1;30;41m Text \u001b[1;30;42m Text \u001b[1;30;43m Text \u001b[1;30;44m Text \u001b[1;30;45m Text \u001b[1;30;46m Text \u001b[1;30;47m Text 
\u001b[1;31;40m Text \u001b[1;31;41m Text \u001b[1;31;42m Text \u001b[1;31;43m Text \u001b[1;31;44m Text \u001b[1;31;45m Text \u001b[1;31;46m Text \u001b[1;31;47m Text 
\u001b[1;32;40m Text \u001b[1;32;41m Text \u001b[1;32;42m Text \u001b[1;32;43m Text \u001b[1;32;44m Text \u001b[1;32;45m Text \u001b[1;32;46m Text \u001b[1;32;47m Text 
\u001b[1;33;40m Text \u001b[1;33;41m Text \u001b[1;33;42m Text \u001b[1;33;43m Text \u001b[1;33;44m Text \u001b[1;33;45m Text \u001b[1;33;46m Text \u001b[1;33;47m Text 
\u001b[1;34;40m Text \u001b[1;34;41m Text \u001b[1;34;42m Text \u001b[1;34;43m Text \u001b[1;34;44m Text \u001b[1;34;45m Text \u001b[1;34;46m Text \u001b[1;34;47m Text 
\u001b[1;35;40m Text \u001b[1;35;41m Text \u001b[1;35;42m Text \u001b[1;35;43m Text \u001b[1;35;44m Text \u001b[1;35;45m Text \u001b[1;35;46m Text \u001b[1;35;47m Text 
\u001b[1;36;40m Text \u001b[1;36;41m Text \u001b[1;36;42m Text \u001b[1;36;43m Text \u001b[1;36;44m Text \u001b[1;36;45m Text \u001b[1;36;46m Text \u001b[1;36;47m Text 
\u001b[1;37;40m Text \u001b[1;37;41m Text \u001b[1;37;42m Text \u001b[1;37;43m Text \u001b[1;37;44m Text \u001b[1;37;45m Text \u001b[1;37;46m Text \u001b[1;37;47m Text 
```
"""
		)
	
		await interaction.response.send_message(
			# 'not implemented yet',
			 embed = embed,
			# ephemeral = True # only for debuggin final version sould send an actual message
		)
	
	# TODO: add a slash command for paginated data
	

async def setup(bot):
	await bot.add_cog( Texts(bot))
