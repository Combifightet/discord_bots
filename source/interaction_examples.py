import discord
from discord.ext import commands
from discord import app_commands
import os

BOT_TOKEN: str = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)


### BUTTON + SELECT MENU VIEW ###
class ExampleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ExampleSelect())

    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.green, custom_id="example:button")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the button!", ephemeral=True)


class ExampleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Option 1", description="First option", value="1"),
            discord.SelectOption(label="Option 2", description="Second option", value="2")
        ]
        super().__init__(placeholder="Choose an option...", options=options, custom_id="example:select")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected: {self.values[0]}", ephemeral=True)


### MODAL (FORM) ###
class ExampleModal(discord.ui.Modal, title="Example Modal Form"):
    name = discord.ui.TextInput(label="Your Name")
    age = discord.ui.TextInput(label="Your Age", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello {self.name.value}, age {self.age.value}!", ephemeral=True)


### CONTEXT MENUS (Declared at module level — NOT in a class) ###
@app_commands.context_menu(name="Greet User")
async def greet_user(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(f"Hello {user.mention}!", ephemeral=True)

@app_commands.context_menu(name="Quote Message")
async def quote_message(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(f"> {message.content}\n— *{message.author}*", ephemeral=True)


### COG FOR COMMANDS & SLASH ###
class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("ExampleCog loaded")

    @commands.command(aliases=["EXAMPLE", "Example"])
    async def example(self, ctx: commands.Context):
        msg = await ctx.send("React with ✅ or ❌ to this message.")
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        await ctx.send("Interact below:", view=ExampleView())

    @app_commands.command(name="modal", description="Open a modal form.")
    async def modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ExampleModal())

    @app_commands.command(name="fruit", description="Choose your favorite fruit.")
    @app_commands.describe(name="Name of the fruit")
    async def fruit(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"You selected {name}", ephemeral=True)

    @fruit.autocomplete("name")
    async def fruit_autocomplete(self, interaction: discord.Interaction, current: str):
        fruits = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
        return [
            app_commands.Choice(name=fruit, value=fruit)
            for fruit in fruits if current.lower() in fruit.lower()
        ]


### SETUP ON READY ###
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")

    # Register persistent view
    bot.add_view(ExampleView())

    # Add cog with slash commands
    await bot.add_cog(ExampleCog(bot))

    # Register context menus
    bot.tree.add_command(greet_user)
    bot.tree.add_command(quote_message)

    # Sync all app commands
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} application commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")


### MAIN ENTRY POINT ###
def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set in environment.")
        return

    bot.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
