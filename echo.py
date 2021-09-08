import asyncio
from discord.ext import commands


token = "[input token here]"
bot = commands.Bot("")


@bot.event
async def on_ready():
	print('Bot is now working!\n')


@bot.event
async def on_message(message):
	if(message.author.id == [put your id here]):
		if(message.content == "//echo"):
			print("Echo mode on")
			while(0x01):
				string = input()
				if(string.lower() != "q"):
					await message.channel.send(string)
				else:
					break
			print("Echo mode off")


bot.run(token)
