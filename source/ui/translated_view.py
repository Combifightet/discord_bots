import discord

from discord.ui import LayoutView

from util.translations import LANGUAGES
from ui.buttons import ToggleButton


class TranslatedView(LayoutView):
	"""Base class for views that support language switching with a toggle button."""
	
	def __init__(self, default_language: str = 'en'):
		super().__init__()
		self.language_code = default_language
		self.toggle_state = (default_language == 'en')  # True = English, False = German
		self._build_view()
	
	def _build_view(self):
		"""Build the view components. Must be implemented by subclasses."""
		self.clear_items()
		self._build_content()
	
	def _build_content(self):
		"""Override this method in subclasses to build the actual content."""
		raise NotImplementedError("Subclasses must implement _build_content()")
	
	def _create_language_toggle(self) -> ToggleButton:
		"""Create a language toggle button with proper labels."""
		return ToggleButton(
			state=self.toggle_state,
			label_on=LANGUAGES['german']['de'],  # Show "switch to German"
			label_off=LANGUAGES['english']['en'],  # Show "switch to English"
			style_on=discord.ButtonStyle.secondary,
			style_off=discord.ButtonStyle.secondary,
			on_changed=self._on_language_change
		)
	
	async def _on_language_change(self, interaction: discord.Interaction, state: bool):
		"""Handle language change from toggle button."""
		print(f'Changed language toggle state to {state} ({"English" if state else "German"})')
		
		# Update both the toggle state and language code
		self.toggle_state = state
		self.language_code = 'en' if state else 'de'
		
		# Rebuild the view with new language
		self._build_view()
		
		# Update the message with the new view
		if interaction.response.is_done():
			await interaction.edit_original_response(view=self)
		else:
			await interaction.response.edit_message(view=self)