import asyncio
from dis import disco
from email import message
from turtle import color, title
import discord
from requests import get
import json
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
from discord.embeds import Embed
from discord import colour
from random import choice, random
import random
import giphy_client
from giphy_client.rest import ApiException
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def is_connected(ctx):
    voice_client = ctx.message.guild.voice_client
    return voice_client and voice_client.is_connected()

client = commands.Bot(command_prefix='$')

status = ['Jamming out to music!', 'Eating!', 'Sleeping!']
queue = []
loop = False

@client.event
async def on_ready():
    change_status.start()
    print('Bot is online!')

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `?help` command for details!')

@client.command(name='giffy', help='This command returns gifs from giffy')
async def giffy(ctx,*,q="Smile"):
    api_key = "tA4tHZ0fVOc4UX1FthsmHgpqLxxhsUKK"
    api_instance = giphy_client.DefaultApi()

    try:
         
        api_response = api_instance.gifs_search_get(api_key, q, limit=5,rating='g')
        lst =list(api_response.data)
        giff = random.choice(lst)
        embed = discord.Embed(title=q)
        embed.set_image(url=f"https://media.giphy.com/media/{giff.id}/giphy.gif")
        await ctx.channel.send(embed=embed)

    except ApiException as r:
        print("Exeption for the api")

@client.command(name='meme', help='This command returns memes')
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.reply(embed=meme)

@client.command(help = "Prints details of Server")
async def where_am_i(ctx):
    owner=str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc=ctx.guild.description
    
    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    await ctx.send(embed=embed)
    members=[]
    async for member in ctx.guild.fetch_members(limit=150) :
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))

punchgifs = ["https://c.tenor.com/w3_5V8KfRO4AAAAC/kick-anime.gif","https://c.tenor.com/_OJw-eCkMYAAAAAC/anime-naruto.gif","https://c.tenor.com/KBo6zdxSC3MAAAAM/spy-x-family-loid-forger.gif","https://c.tenor.com/4zwRLrLMGm8AAAAC/chifuyu-chifuyu-kick.gif"]
punch_name =["Punches You!"]
birthdaygifs =["https://c.tenor.com/Uk21ev0V32cAAAAd/happy-birthday.gif"]
birthday_word =["A crazy girl is celebrating another birthday ..... happy birthday lamia 😝"]
slapgifs = ["https://c.tenor.com/XiYuU9h44-AAAAAC/anime-slap-mad.gif","https://c.tenor.com/iDdGxlZZfGoAAAAC/powerful-head-slap.gif","https://c.tenor.com/FJsjk_9b_XgAAAAC/anime-hit.gif","https://c.tenor.com/1-1M4PZpYcMAAAAd/tsuki-tsuki-ga.gif","https://c.tenor.com/LUJRVpYgy-8AAAAC/kiniro-kiniro-mosaic.gif"]
slap_name =["Slap you!","Palms you!","wollops you"]

shemiqqx =["https://c.tenor.com/Ghi9dv-E-iIAAAAS/ryder-san-andreas.gif"]
gifs =[
        "https://tenor.com/view/dogs-cute-all-you-need-is-love-gif-13111410",
        "https://tenor.com/view/puppy-high-five-cute-fluffy-gif-10903022",
        "https://media.discordapp.net/attachments/730945069711884289/808982584280350730/image0.gif",
        "https://tenor.com/view/puppies-silly-puppy-cute-puppy-doggys-dogs-gif-17639683",
        "https://tenor.com/view/golden-retriever-dog-did-you-call-me-mirame-perrito-golden-gif-17047579",
        "https://tenor.com/view/bedtime-sleepy-good-night-sleep-well-go-to-bed-gif-15801983",
        "https://tenor.com/view/look-puppy-hi-hello-gif-5047026",
        "https://tenor.com/view/dog-getting-frustrated-stop-it-annoyed-gif-15192974"
    ]

sleeps = [
		"https://c.tenor.com/zKDUIhAzmDEAAAAd/sleepy-baby-sleepy-babe.gif",
		"https://c.tenor.com/iE-4pXEdUykAAAAC/cat-couverture.gif",
		"https://c.tenor.com/5h6DPGp-5ugAAAAC/tkthao219-peach.gif"	]
@client.command(name='gif', help='return random gif')
async def gif(ctx):
    await ctx.send(random.choice(gifs))

@client.command(name='shemiqq', help='shemiqq')
async def shemiqq(ctx):
    await ctx.send(random.choice(shemiqqx))

@client.command(name='punch', help='This command kick someone from the server jk hahaha!')
async def punch(ctx):
    embed = discord.Embed(description = f"{ctx.author.mention} {random.choice(punch_name)}",color = discord.Color.random())
    embed.set_image(url=(random.choice(punchgifs)))
    await ctx.send(embed = embed)

@client.command()
async def birthday(ctx):
    embed = discord.Embed(description = f"{random.choice(birthday_word)}",color = discord.Color.random())
    embed.set_image(url=(random.choice(birthdaygifs)))
    await ctx.send(embed = embed)

@client.command(name='slap', help='This command slap someone from the server')
async def slap(ctx):
    embed = discord.Embed(description = f"{ctx.author.mention} {random.choice(slap_name)}",color = discord.Color.random())
    embed.set_image(url=(random.choice(slapgifs)))
    await ctx.send(embed = embed)


@client.command(name='sleep', help='This command return sleep')
async def sleep(ctx):
    embed = discord.Embed(description = f"{ctx.author.mention} is going to sleep",color = discord.Color.random())
    embed.set_image(url=(random.choice(sleeps)))
    await ctx.send(embed = embed)

@client.command(name='howgay', help='return how gay are you')
async def howgay(ctx):
    embed = discord.Embed(title="Gayrate",description = f"you are {random.randrange(101)}% Gay {ctx.author.mention}",color = discord.Color.random())
    await ctx.send(embed = embed)


@client.command(name='cool', help='return how cool are you')
async def howcool(ctx):
    embed = discord.Embed(title="Cool",description = f"you are {random.randrange(101)}% Cool {ctx.author.mention}",color = discord.Color.random())
    await ctx.send(embed = embed)

@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['***grumble*** Why did you wake me up?', 'Top of the morning to you lad!', 'Hello, how are you?', 'Hi', '**Wasssuup!**']
    await ctx.send(choice(responses))

@client.command(name='die', help='This command returns a random last words')
async def die(ctx):
    responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
    await ctx.send(choice(responses))


@client.command(name='credits', help='This command returns the credits')
async def credits(ctx):
    await ctx.send('Made by `Sunlight`')
    await ctx.send('Thanks to `lamia` for coming up with the idea')
    await ctx.send('Thanks to `server` for helping with the bot and')

@client.command(name='creditz', help='This command returns the TRUE credits')
async def creditz(ctx):
    await ctx.send('**No one but me, lozer!**')

@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()
# @client.command(name='gif',help='This commad start a guessing game')

@client.command(name='leave', help='This command stops the music and makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='loop', help='This command toggles loop mode')
async def loop_(ctx):
    global loop

    if loop:
        await ctx.send('Loop mode is now `False!`')
        loop = False
    
    else: 
        await ctx.send('Loop mode is now `True!`')
        loop = True

@client.command(name='play', help='This command plays music')
async def play(ctx):
    global queue

    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    elif len(queue) == 0:
        await ctx.send('Nothing in your queue! Use `?queue` to add a song!')

    else:
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        except: 
            pass

    server = ctx.message.guild
    voice_channel = server.voice_client
    while queue:
        try:
            while voice_channel.is_playing() or voice_channel.is_paused():
                await asyncio.sleep(2)
                pass

        except AttributeError:
            pass
        
        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(queue[0], loop=client.loop)
                voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                
                if loop:
                    queue.append(queue[0])

                del(queue[0])
                
            await ctx.send('**Now playing:** {}'.format(player.title))

        except:
            break

@client.command(name='volume', help='This command changes the bots volume')
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("Not connected to a voice channel.")
    
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")

@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@client.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@client.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@client.command(name='queue')
async def queue_(ctx, *, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')

@client.command(name='remove')
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')
    
    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')

@client.command(name='view', help='This command shows the queue')
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


client.run('OTU1ODAwNjA3OTQ2NTkyMzA2.Yjm8rg.PxElD5AZ_rkPB9krc88AtHzImoU')