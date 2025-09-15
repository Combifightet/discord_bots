import discord
from discord.ext import commands
from discord import app_commands
import math

from util.pagination import PaginatedView



class Examples(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Loaded Examples cog')
        
        # Generate sample data (64 items as requested)
        self.sample_data = []
        statuses = ["Active", "Inactive", "Pending", "Error"]
        
        for i in range(1, 65):  # Example 1 to 64
            self.sample_data.append({
                "id": i,
                "name": f"Example {i}",
                "value": f"Val_{i:03d}",
                "status": statuses[(i - 1) % len(statuses)]
            })

    @app_commands.command(name='colors', description='display all text and background colors')
    async def colors(self, interaction: discord.Interaction):
        """Slash command to display all possible text and background colors"""

        embed: discord.Embed = discord.Embed(
            title='Text Colors',
            url='https://www.pythondiscord.com/pages/guides/python-guides/discord-messages-with-colors/',
            description="""
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

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name = 'pagination',description = 'Display paginated data with navigation buttons')
    @app_commands.describe(items_per_page = 'The word to be looked up')
    async def pagination(self, interaction: discord.Interaction, items_per_page: int = 10):
        """Slash command to display paginated data"""

        await PaginatedView(
            interaction=interaction,
            total_pages=5
        ).setup()




    @app_commands.command(name = 'buttons',description = 'Display all possible button styles')
    @app_commands.describe(enabled = 'Weather the buttons are enabled or disabled')
    async def buttons(self, interaction: discord.Interaction, enabled:bool = True):
        """Slash command to display all possible discord embed button styles"""

        await ButtonsView(interaction=interaction, enabled=enabled).setup()



async def setup(bot):
    await bot.add_cog(Examples(bot))



### Buttons View Class ###

class ButtonsView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, enabled: bool = True):
        self.interaction = interaction
        self.enabled = enabled
        super().__init__(timeout=300)  # doesn't accept new interaction after <timeout> seconds

        link_button = discord.ui.Button(
            emoji = '5️⃣',
            label = 'link / _url_',
            style = discord.ButtonStyle.link,
            url = 'https://github.com/combifightet',
            disabled=not self.enabled
        )
        self.add_item(link_button)

        premium_button = discord.ui.Button(
            style = discord.ButtonStyle.premium,
            sku_id = 1416080458093170820, # 'buy me a coffe'
            disabled = not self.enabled
        )
        self.add_item(premium_button)

    @discord.ui.button(emoji='1️⃣', label='primary / _blurple_', style=discord.ButtonStyle.primary)
    async def primary(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='2️⃣', label='secondary / _grey_ / _gray_', style=discord.ButtonStyle.secondary)
    async def secondary(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='3️⃣', label='success / _green_', style=discord.ButtonStyle.success)
    async def success(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='4️⃣', label='danger / _red_', style=discord.ButtonStyle.danger)
    async def danger(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    async def setup(self):
        # Set the disabled state of all buttons after initialization
        for item in self.children:
            item.disabled = not self.enabled

        embed:discord.Embed = discord.Embed(
            title='Buttons - Example',
            description='A small Embed to display all 6 different button types',
            colour=0xac91b4
        )
        embed.set_author(
            name='Combifightet',
            url='https://github.com/combifightet',
            icon_url='https://avatars.githubusercontent.com/u/47188809'
        )
        await self.interaction.response.send_message(embed=embed, view=self)



    async def on_timeout(self):
        # Disable all buttons when view times out
        # for item in self.children:
        #     item.disabled = True
        pass
