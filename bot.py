import os
import discord
from discord.ext import commands
from google import genai

# سحب المفاتيح بأمان من إعدادات السيرفر
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=message.content,
                )
                await message.channel.send(response.text)
            except Exception as e:
                await message.channel.send(f"Error: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
