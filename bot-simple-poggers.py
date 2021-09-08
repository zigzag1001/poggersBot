# bot.py
import os
import random
from time import sleep
import asyncio
import time
import youtube_dl

import discord
from discord.ext import commands
from discord.utils import get

TOKEN = "[input token here]"
justUsed = ""
connected = False
playGachi = True
optoutusers = []

bot = commands.Bot(command_prefix='pog, ')
def openThing(fileName):
    global justUsed
    notGood = True
    with open('.\\media\\' + fileName) as Links:
        words = Links.read().split(",")
        while notGood:
            response = random.choice(words)
            if response != justUsed:
                notGood = False
        print(response)
    justUsed = response
    return response

async def mp3Player(fileName, message, length, directory):
    try:
	    global vc
	    global connected
	    global playGachi
	    user = message.author
	    print(user)
	    voice_channel = user.voice.channel
	    print(voice_channel)
	    channel = None
	    if voice_channel != None:
	        channel = voice_channel.name
	        if not connected:
	            vc = await voice_channel.connect()
	            connected = True
	        if directory == 0:
	            vc.play(discord.FFmpegPCMAudio(".\\mp3\\"+fileName))
	        elif directory == 1:
	            vc.play(discord.FFmpegPCMAudio("M:\\Gachi\\"+fileName))
	        elif directory == 2:
	        	vc.play(discord.FFmpegPCMAudio(".\\minecraft\\"+fileName))
	        elif directory == 3:
	        	vc.play(discord.FFmpegPCMAudio(".\\mp3\\yt\\"+fileName))

	        if (directory != 0 or directory != 3) and length == 0:
	            while vc.is_playing():
	                await asyncio.sleep(1)
	            vc.stop()
	        elif directory != 0 or directory != 3:
	            await asyncio.sleep(length)
	            vc.stop()
	        elif length == 0:
	            while vc.is_playing():
	                await asyncio.sleep(1)
	            await vc.disconnect()
	            connected = False
	        else:
	            await asyncio.sleep(length)
	            await vc.disconnect()
	            connected = False
    except:
        try:
            vc.stop()
            await vc.disconnect()
            connected = False	
            playGachi = False
            pass
        except:
        	await vc.disconnect()
        	connected = False
        	pass
        print("whoop exception at mp3Player")
    await vc.disconnect()
    connected = False

def checkifplaying():
	return vc.is_playing()

with open('optout.txt') as optoutList:
	optoutusers = optoutList.read().split(",")

@bot.event
async def on_ready():
    print('Bot is now working!')
    await bot.change_presence(activity=discord.Game('with your dad ;)'))

@bot.event
async def on_message(message):
    with open('optout.txt') as optoutList:
       optoutusers = optoutList.read().split(",")
    global messagem
    if message.author == bot.user or ('.com' in message.content and not 'play' in message.content.lower()):
        return
    if message.author == 327606483741179914 and random.randint(0, 2) == 1:
        print("thompson denied")
        return
    if str(message.author) in optoutusers and not "pog, " in message.content.lower():
    	print(str(message.author), "is opted out")
    	return

    messagem = message

    #==============================poggers

    if 'poggers' in message.content.lower():
            
        response = openThing('poggers.tenor')

        unpoggers = ["https://tenor.com/view/poggers-deku-bakugo-my-hero-academia-my-hero-gif-18930451",
                     "https://tenor.com/view/unpoggers-pog-gif-19224204",
                     "https://tenor.com/view/anime-poggers-anime-poggers-anime-gif-18290524"]

        await message.channel.send(response)
        
        if response in unpoggers:
            await message.channel.send("whoa!")
            await message.channel.send("unpoggers...")

        else:
            await mp3Player("poggers.mp3", message, 1.2, 0)
            chance = random.randint(1, 50)
            print(chance)
            if chance == 24:
                await message.channel.send("poggers", tts=True)

        #==============================amogus

    elif 'amogus' in message.content.lower():

        a = random.choice(["amoguss", "aamogus", "sus", "amogus"])

        await mp3Player(a + ".mp3", message, 0, 0)

        await message.channel.send("ඞ")

    await bot.process_commands(message)


@bot.command(help='tells (un)funny joke')
async def funny(ctx):
    await mp3Player(random.choice(["eel.mp3", "congrats.mp3", "ahhhh.mp3"]), messagem, 0, 0)

@bot.command(help="play command, plays mp3's from playlist, opt. seconds")
async def playmp3(ctx, fileName: str, seconds: float = 0):
	fileName.replace(".mp3", "")
	fileName = fileName + ".mp3"
	print(fileName)
	await mp3Player(fileName, messagem, seconds, 0)

@bot.command(help="youtube play command, only accepts url")
async def play(ctx, url: str):
	if "list" in url:
		url = url[:url.index("list")-1]
	songDownloaded = os.path.isfile("ytsong.mp3")
	try:
		if songDownloaded:
			os.remove("ytsong.mp3")
	except PermissionError:
		await ctx.send("oop gotta wait for this one to end. or like use stop command idk")
	ytdl_opts = {
	'format': 'bestaudio/best',
	'outtmpl': '.\\mp3\\yt\\ytsong.%(ext)s',
	'postprocessors': [{
	'key': 'FFmpegExtractAudio',
	'preferredcodec': 'mp3',
	'preferredquality': '192'
		}]
	}
	print("downloading", url)
	with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
		ydl.download([url])
	await mp3Player('ytsong.mp3', messagem, 0, 3)


@bot.command(help='audio files you can play')
async def playlist(ctx):
    files = os.listdir(".\\mp3\\")
    await messagem.channel.send(files)

@bot.command(help='stop playing')
async def stop(ctx):
    global playGachi
    global playMinecraft
    global connected
    playGachi = False
    playMinecraft = False
    vc.stop()
    await vc.disconnect()
    connected = False

@bot.command(help='triggers list')
async def triggers(ctx):
    with open("triggers.txt") as triggers:
        response = triggers.read().split(",")
    await messagem.channel.send("this is the simple version of this bot, so most of these wont work")
    await messagem.channel.send(response)

''' Check bot-og.py for why this is commented out
@bot.command(help='gachi')
async def gachi(ctx):
    global playGachi
    global connected
    global vc
    m = messagem
    playGachi = True
    while playGachi:
        toPlay = random.choice(os.listdir("M:\\Gachi"))
        await m.channel.send(toPlay)
        await mp3Player(toPlay, messagem, 0, 1)
'''

@bot.command(help='minecraft')
async def minecraft(ctx):
	global playMinecraft
	global connected
	global vc
	m = messagem
	playMinecraft = True
	listofsongs = os.listdir(".\\minecraft")
	if listofsongs == []:
		playMinecraft = False
	while playMinecraft:
		toPlay = random.choice(listofsongs)
		listofsongs.remove(toPlay)
		await m.channel.send(toPlay)
		await mp3Player(toPlay, messagem, 0, 2)

@bot.command(help='opt out using this')
async def optout(ctx):
	with open('optout.txt') as optoutList:
		optoutusers = optoutList.read().split(",")
	print(optoutusers)
	if not str(messagem.author) in optoutusers:
		with open('optout.txt', 'a') as optoutList:
			optoutList.write(str(messagem.author) + ',')
	await messagem.channel.send('opt back in using "pog, optin"')

@bot.command(help='opt back in')
async def optin(ctx):
	with open('optout.txt') as optoutList:
		optoutusers = optoutList.read().split(",")
	print(optoutusers)
	new = ''
	if str(messagem.author) in optoutusers:
		optoutusers.remove(str(messagem.author))
	for i in optoutusers:
		if i != '':
			new += i + ','
	with open('optout.txt', 'w') as optoutList:
		optoutList.write(new)
	await messagem.channel.send("welcome back!")

@bot.command(help='random screenshot')
async def randomsc(ctx, n: int = 1):
	letters = "qwertyuiopasdfghjklzxcvbnm"
	for i in range(n):
		await ctx.send("https://prnt.sc/" + random.choice(letters) + random.choice(letters) + str(random.randint(1000, 9999)))

bot.run(TOKEN)
