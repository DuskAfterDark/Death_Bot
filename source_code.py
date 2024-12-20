import discord
from datetime import datetime, timedelta
import random

TOKEN = '0'

intents = discord.Intents.default()

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

user_predictions = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s) globally.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(
        title="Hello, and thank you for using Death Bot",
        description=(
            "I can predict your time of death.\n\n"
            "To see your death date use `/predict` to get started. \n\n"
            "You can only predict **once**, and thats it."
        ),
        color=discord.Color.from_rgb(0, 0, 0)
    )
    embed.set_footer(text="Thank you for inviting me!")
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=embed)
            break

@tree.command(name="predict", description="Predicts a fictional time of death within 100 years.")
async def predict(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id in user_predictions:
        await interaction.response.send_message(
            f"{interaction.user.mention}, you already predicted! Your time of death is: {user_predictions[user_id]}"
        )
    else:
        random_days = random.randint(1, 36500)
        random_seconds = random.randint(0, 86400)
        death_time = datetime.now() + timedelta(days=random_days, seconds=random_seconds)
        formatted_date = death_time.strftime("%A, %d %B %Y, at %I:%M:%S %p")

        user_predictions[user_id] = formatted_date

        await interaction.response.send_message(
            f"{interaction.user.mention}, your predicted time of death is: {formatted_date}."
        )

bot.run(TOKEN)
