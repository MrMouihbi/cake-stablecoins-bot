import discord
from discord.ext import commands
from asyncio import sleep
import cake


# Add the token of the bot :
token = ""
client = commands.Bot("_")

# Add rooms id, expl : rooms = [824417505367031868, 826321502037036547]
rooms = []


@client.event
async def on_ready():
    print('Bot is online.')


async def get_stats():
    result = cake.getStats()
    if result == [] :
      return
    
    embed = discord.Embed(
        #title = "Live Stats" ,
        description = "You can now place your liquidity in the pools with the best ROIs :blush:",
        color = discord.Color.blue()
    )
    embed.set_author(name="Pancakeswap Stable Coins LP Rewards", icon_url="https://cdn.discordapp.com/attachments/489932450617884673/828589749241118760/ck2.webp" )
    for x in result:
        embed.add_field(
            name=(':cupcake: '+x['base_symbol']+'-'+x['quote_symbol']+' pool:'),
            value = ("***Last price:"+f"{x['last_price']:.4f}***\n\n"+
                    "**For each $1000 provided as liquidity you get:**\n\n"+
                    f':coin: ***__per day:__ {x["daily_fees_per_1k"]:.5f} '+x['quote_symbol']+"*** "+
                    f'\n:clock10: ***__daily roi:__ {x["daily_roi"]:.5f}%***'+
                    f'\n:moneybag: ***__annual roi:__ {x["annual_roi"]:.2f}%***'+
                    '\n\n _'
                    ),
            inline=False)
    
    embed.set_footer(text="Stats are always calculated according to the last 24h")
    for x in rooms:
        try:
            channel = client.get_channel(x)
            await channel.send(embed=embed)
        except:
            pass


async def display_stats():
   await client.wait_until_ready()
   while not client.is_closed():
        await get_stats()
        await sleep(14400) #each 4 H

#required : to keep the looping of the function work
client.loop.create_task(display_stats())

client.run(token)