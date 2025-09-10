import discord
from discord.ext import commands
from discord import app_commands
import math


class PaginationView(discord.ui.View):
    def __init__(self, data, items_per_page=10):
        super().__init__(timeout=300)  # 5 minute timeout
        self.data = data
        self.items_per_page = items_per_page
        self.current_page = 0
        self.max_pages = math.ceil(len(data) / items_per_page)
        
        # Update button states
        self.update_buttons()
    
    def update_buttons(self):
        # Disable/enable buttons based on current page
        self.first_page.disabled = self.current_page == 0
        self.prev_page.disabled = self.current_page == 0
        self.next_page.disabled = self.current_page >= self.max_pages - 1
        self.last_page.disabled = self.current_page >= self.max_pages - 1
    
    def get_current_page_data(self):
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.data[start_idx:end_idx]
    
    def create_embed(self):
        current_data = self.get_current_page_data()
        
        embed = discord.Embed(
            title="📊 Paginated Data",
            color=0x00ff88,
            description=f"Showing items {self.current_page * self.items_per_page + 1}-{min((self.current_page + 1) * self.items_per_page, len(self.data))} of {len(self.data)}"
        )
        
        # Create tabulated data display
        data_text = "```\n"
        data_text += f"{'ID':<4} | {'Name':<12} | {'Value':<10} | {'Status':<8}\n"
        data_text += "-" * 42 + "\n"
        
        for item in current_data:
            data_text += f"{item['id']:<4} | {item['name']:<12} | {item['value']:<10} | {item['status']:<8}\n"
        
        data_text += "```"
        
        embed.add_field(
            name="Data Table",
            value=data_text,
            inline=False
        )
        
        embed.set_footer(text=f"Page {self.current_page + 1}/{self.max_pages}")
        
        return embed
    
    @discord.ui.button(label='⏮️', style=discord.ButtonStyle.gray, disabled=True)
    async def first_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = 0
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label='◀️', style=discord.ButtonStyle.primary, disabled=True)
    async def prev_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label='🔢', style=discord.ButtonStyle.secondary)
    async def page_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"Currently on page **{self.current_page + 1}** of **{self.max_pages}**\n"
            f"Total items: **{len(self.data)}**",
            ephemeral=True
        )
    
    @discord.ui.button(label='▶️', style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label='⏭️', style=discord.ButtonStyle.gray)
    async def last_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = self.max_pages - 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    async def on_timeout(self):
        # Disable all buttons when view times out
        for item in self.children:
            item.disabled = True


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
        print(f'Pagination command invoked by {interaction.user} with items_per_page={items_per_page}')
        
        # Validate items_per_page
        if items_per_page < 1 or items_per_page > 25:
            await interaction.response.send_message(
                "❌ Items per page must be between 1 and 25!",
                ephemeral=True
            )
            return
        
        # Create the pagination view
        view = PaginationView(self.sample_data, items_per_page)
        embed = view.create_embed()
        
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Examples(bot))
