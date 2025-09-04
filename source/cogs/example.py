import discord
from discord.ext import commands


class Example(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print('Loaded Example cog')

	@commands.command(aliases=['EXAMPLE', 'Example'])
	async def example(self, ctx):
		await ctx.send('`<missing example>`')
	

async def setup(bot):
	await bot.add_cog(Example(bot))
