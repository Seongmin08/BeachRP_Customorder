import discord, asyncio, sqlite3, datetime, json, time
from discord.ext import commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
token = 'MTAzMzk5NTkxNzQ3ODYxMzA0Mg.Gl4Gtm.KZstapwxh3PfIAmOBtsOEg7YOMSOQZXBc-0wig'

@client.event
async def on_ready():
    print("Bot test")

@client.command()
async def 사전예약(ctx) :
    await ctx.message.channel.send("{}, **DM을 확인해주세요.**".format(ctx.author.mention))
    embed = discord.Embed(title = f"{ctx.author.name}님의 사전예약이 완료되었습니다!",
    description = "사전예약은 서버 오픈전에만 효력이 있습니다.", color = 0x62c1cc)
    embed.add_field(name = "보상은 인게임 머니 10억, 사전예약 전용 한정스킨, 한정차량", value = "서버 오픈후 이 메시지를 제출해 보상을 받을수있습니다!")
    embed.set_footer(text = "2023 : Candy")
    await ctx.author.send(f'<@{ctx.author.id}>', embed = embed)

client.run (token)
