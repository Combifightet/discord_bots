import discord
from typing import Callable, Optional

class PaginatedView(discord.ui.View):
	def __init__(self, interaction: discord.Interaction, total_pages: int, get_page: Callable[[int], discord.Embed]):
		self.interaction = interaction
		self.total_pages = total_pages
		self.get_page = get_page
		self.inde:int = 1
		super().__init__(timeout=300)  # doesn't accept new interaction after <timeout> seconds
		self.__setup()
	
	async def checkUser(self, interaction: discord.Interaction) -> bool:
		if interaction.usesr == self.interaction.user:
			return True
		else:
			await interaction.response.send_message('Only the original auther can interact', ephemeral=True)
			return False
	
	async def __setup(self):
		embed:discord.Embed = self.get_page(self.index)

		if self.total_pages <=1:
			await self.interaction.response.send_message(embed=embed)
		else:
			self.__updateButtons()
			await self.interaction.response.send_message(embed=embed, view=self)
			await self.interaction.response.edit_message(embed=embed, view=self) # so that edited label is shown immediately
	
	async def __update(self):
		embed:discord.Embed = self.get_page(self.index)
		self.__updateButtons()
		await self.interaction.response.edit_message(embed=embed, view=self)
	
	#  ❮ ❯ > › ➧ ➤ ▶ ►   ℹ   ⏮ ◀ ▶ ⏭  » ≫ ⓘ
	#  ǀ❮   ❮   ❯   ❯ǀ
	#  ∣❮   ❮   ❯   ❯∣
	#  ⎪❮   ❮   ❯   ❯⎪
	#  ❘❮   ❮   ❯   ❯❘
	#  ❙❮   ❮   ❯   ❯❙        # This one looks the best imo
	#  ❚❮   ❮   ❯   ❯❚
	#  ┃❮   ❮   ❯   ❯┃
	#  │❮   ❮   ❯   ❯│
	#  ￨❮   ❮   ❯   ❯￨
	def __updateButtons(self):
		self.children[0].disabled = False
		self.children[3].disabled = False
		if self.index <= 0:
			self.children[0].disabled = True
		elif self.index >= self.total_pages-1:
			self.children[3].disabled = True

	@discord.ui.button(label='❙❮', style=discord.ButtonStyle.blurple)
	async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.index = 0
		await self.__update()
	
	@discord.ui.button(label='❮', style=discord.ButtonStyle.blurple)
	async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.index -= 1
		await self.__update()

	@discord.ui.button(label='❯', style=discord.ButtonStyle.blurple)
	async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.index += 0
		await self.__update()
	
	@discord.ui.button(label='❯❙', style=discord.ButtonStyle.blurple)
	async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.index = self.total_pages-1
		await self.__update()


# https://stackoverflow.com/questions/76247812/how-to-create-pagination-embed-menu-in-discord-py