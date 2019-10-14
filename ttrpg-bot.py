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
    '''Takes a rolled value, and the face total of a die roll, checks to see if it explodes, and returns the result of the explosion as a string'''

    if result == die:
        return str(result) + ' + ' + str(explode(random.randint(1, die), die))
    else:
        return result

def roll(num, die, adv = 0):
    '''Rolls a given die, num, number of times, checking for explosions and allowing for adv/disadvantage'''
    
    #Unsure of input type, so all converted to ints.
    num = int(num)
    die = int(die)
    adv = int(adv)
    
    roll_list = []

    #Create the random values for the roll (inc. adv/dis)
    for i in range(0, num + abs(adv)):
        roll_list.append(random.randint(1, die))
    current = roll_list
    
    #Check to see if there is advantage or disadvantage, and subtract the appropriate values
    if adv > 0:
        roll_list.sort()
    elif adv < 0:
        roll_list.sort(reverse=True)
    final_roll_list = [explode(x, die) for x in roll_list[abs(adv)::]]
    
    #Checks to see if an explosion happened and a string was returned, handles it, then returns a tuple containing the results at various stages
    output = 0
    for v in final_roll_list:
        if type(v) is str:
            output += eval(v)
        else:
            output += v
    return (current, final_roll_list, output)

def parse_dice(text):
    '''Checks to see if adv/disadvantage is required, then passes the correct values to roll()'''
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
    '''Reads in the users messages, checks to see if a request for a roll is made, and performs the roll using the parse_text function'''
    if message.author == client.user:
        return
    try:
        if message.content.startswith('/r '):
            text = message.content[3::].lower()
            output = []
            if '+' in text:
                dice_list = text.split('+')
                for dice in dice_list:
                    dice = dice.strip()
                    output.append(parse_dice(dice))
                initial = []
                adv = []
                final = []
                for result in output:
                    initial.append(result[0])
                    adv.append(result[1])
                    final.append(result[2])
                init_str = ''
                adv_str = ''
                final_str = 0
                for result in initial:
                    init_str += str(result) + ' + '
                init_str = init_str[:-2]
                for result in adv:
                    adv_str += str(result) + ' + '
                adv_str = adv_str[:-2]
                for result in final:
                    final_str += result
                final_str = str(final_str)
                str_out = 'You rolled ' + init_str + 'initially' + '\n' \
                    'This became ' + adv_str + 'after advantage' + '\n' \
                        'Your final result was: ' + final_str
                await message.channel.send(str_out)
            else:
                output = parse_dice(text)
                await message.channel.send('You rolled ' + str(output[0]) +  ' initially\nThis became ' + str(output[1]) + ' after advantage\nYour final result was: ' + str(output[2]))
    except:
        await message.channel.send('Command Unrecognised')
client.run(TOKEN)