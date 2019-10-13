import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

def explode(result, die):
    if result == die:
        return str(result) + ' + ' + str(explode(random.randint(1, die), die))
    else:
        return result

def roll(num, die, adv = 0):
    num = int(num)
    die = int(die)
    adv = int(adv)
    roll_list = []
    for i in range(0, num + abs(adv)):
        roll_list.append(random.randint(1, die))
    current = roll_list
    
    if adv > 0:
        roll_list.sort()
    elif adv < 0:
        roll_list.sort(reverse=True)
    final_roll_list = [explode(x, die) for x in roll_list[abs(adv)::]]
    
    final_roll_list
    
    output = 0
    for v in final_roll_list:
        if type(v) is str:
            output += eval(v)
        else:
            output += v
    return (current, final_roll_list, output)

def parse_dice(text):
    if 'adv' in text:
        dice, adv = text.split('adv')
        num, die = dice.split('d')
        return roll(num, die, adv)
    elif 'dis' in text:
        dice, adv = text.split('dis')
        num, die = dice.split('d')
        return roll(num, die, -int(adv))
    else:
        num, die = text.split('d')
        return roll(num, die)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('/rv '):
        text = message.content[4::].lower()
        output = []
        if '+' in text:
            dice_list = text.split('+')
            for dice in dice_list:
                output.append(parse_dice(dice))
        else:
            output = parse_dice(text)
            await message.channel.send('You rolled ' + str(output[0]) +  ' originally\nThis became ' + str(output[1]) + ' after advantage\nYour final result was: ' + str(output[2]))
    if message.content.startswith('/r '):
        text = message.content[3::].lower()
        output = []
        if '+' in text:
            dice_list = text.split('+')
            for dice in dice_list:
                output.append(parse_dice(dice))
        else:
            output = parse_dice(text)
            await message.channel.send('You rolled ' + str(output[2]))

client.run(TOKEN)