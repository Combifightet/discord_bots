import discord
from discord import app_commands
from discord.ext import commands

from discord.ui import *


from util.translations import HELP_LANGUAGES
from ui.translated_view import TranslatedView


class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print('Loaded Help cog')


	@app_commands.command(name='help', description='Open the help dialog')
	async def test(self, interaction: discord.Interaction):
		await interaction.response.defer(ephemeral=True)  # <- important (makes the bot say its thinking)

		await interaction.followup.send(
			view=HelpView(),
			ephemeral=True
		)

async def setup(bot):
	await bot.add_cog(Test(bot))


class HelpView(TranslatedView):
	'''Help view that extends TranslatedView for language switching.'''
	
	def _build_content(self):
		'''Build the help view content with current language.'''

		# TODO: make selected option persistent on rebuild due to language change
		help_type_select = discord.ui.Select(
			options=[
				discord.SelectOption(label=HELP_LANGUAGES['select_option_1'][self.language_code], description='/modul [name]'),
				discord.SelectOption(label=HELP_LANGUAGES['select_option_2'][self.language_code], description='/search [name]'),
				discord.SelectOption(label=HELP_LANGUAGES['select_option_3'][self.language_code], description='/filter [name]'),
				discord.SelectOption(label=HELP_LANGUAGES['select_option_4'][self.language_code], description='/semesterplan'),
				discord.SelectOption(label=HELP_LANGUAGES['select_option_5'][self.language_code])
			]
		)

		async def select_callback(interaction: discord.Interaction):
			await interaction.response.send_message(
				f'You selected: {help_type_select.values[0]}', ephemeral=True
			)

		help_type_select.callback = select_callback

		self.add_item(
			Container(
				Section(
					TextDisplay(
						f'# {HELP_LANGUAGES['help'][self.language_code]}'
					),
					accessory=self._create_language_toggle()
				),
				Separator(),
				TextDisplay(
					HELP_LANGUAGES['description'][self.language_code]
				),
				ActionRow(help_type_select),
				accent_color=0x4378d5,
			),
		)
