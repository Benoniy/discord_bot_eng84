# BasicBot

# import commands
import logging
import discord
# from regex import regex
import asyncio
import random
import yaml
from aiohttp import ClientSession

from discord.ext import commands, tasks
from discord.colour import Colour
from typing import Optional, Literal

import group_picker

# import bot_commands


logging.basicConfig(filename="log.txt", level=logging.DEBUG, filemode="w")

# Global Variables
# client = discord.Client()
TOKEN = ""
BOT_PREFIX = "+"
URBAN_API_KEY = ""

bot = commands.Bot(command_prefix=BOT_PREFIX)


def setup():
    """ Get token & prefix from file and assigns to variables """
    with open("tokens.yaml") as stream:

        global TOKEN
        global BOT_PREFIX
        global URBAN_API_KEY
        try:
            io = yaml.safe_load(stream)
            logging.info(io)
            TOKEN = io.get('token')
            BOT_PREFIX = io.get('prefix')
            URBAN_API_KEY = io.get('urban_api_key')
            print(f"{URBAN_API_KEY=}")

        except yaml.YAMLError as exc:
            print(exc)
            logging.error(exc)

        # TOKEN = file.readline().replace("\n", "")

        # global BOT_PREFIX
        # BOT_PREFIX = file.readline().replace("\n", "")
        # file.close()
        logging.info(f"Bot token '{TOKEN}' and prefix '{BOT_PREFIX}' are set")


@bot.command(name='clear', help='Used to clear the page for x minutes')
async def clear(context, minutes: Optional[int] = 5):
    """ Sending large message to clear screen temporarily """
    message = await context.channel.send(
            ".\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n."
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n."
            )
    # Waiting time in minutes
    await asyncio.sleep(minutes * 60)
    # Delete message after wait
    await message.delete()


@bot.command(name='groups', help='Try to create groups of x many people. Default to groups of 2')
async def groups(context, *, number_of_people: Optional[int] = 2):
    """ Pick groups """
    if number_of_people < 1:
        await context.channel.send('Number of people in groups must be above 0')
    else:
        await context.channel.send(group_picker.gen_groups(number_of_people))


class NumeberWithThreshold(commands.Converter):
    async def convert(self, context, argument, threshold=100):
        argument = int(argument)
        return argument if argument <= threshold else threshold


class SidesNumber(NumeberWithThreshold):
    async def convert(self, *args):
        return await super().convert(*args, threshold=120)


class DiceNumber(NumeberWithThreshold):
    async def convert(self, *args):
        return await super().convert(*args, threshold=20)


@bot.command(name='roll', help='Roll y dice of x sides.', aliases=["rol"])
async def roll_dice(context, x: Optional[SidesNumber] = 6, y: Optional[DiceNumber] = 1):
    """ Rolls a specified number of user defined dice

        If x or y is not a digit, it will take the default value of 6 and 1 respectively
        Additionally, sides and dice have max values of 120 and 20. If the input surpasses the
        max values, they automatically get assinged their max value

    """
    # print(x, y)
    if x > 0 and y > 0:

        to_send = "Rolled:\n"
        for die in range(y):
            roll = random.randint(1, x)
            to_send += "{0},\n".format(roll)
        to_send = to_send[:-2]
        await context.channel.send(to_send)
    else:
        await context.channel.send("Invalid input")


@bot.command(name="flip", help="Return head or tails")
async def flip_coin(context):
    """ Flips a coin and displays the result """
    to_send = ""
    flip = bool(random.getrandbits(1))

    if flip:
        to_send += "Heads!"
    else:
        to_send += "Tails!"

    await message.channel.send(to_send)


@bot.command(name="agile", help="List agile values")
async def agile(context):
    await context.channel.send("Whilst there is value to the items on the right, we should value items on the left more!\n"
                               f"1. {'`Individuals and Interactions`':>30} over `Processes and Tools`\n"
                               f"2. {'`Working Software`':>42} over `Comprehensive Documentation`\n"
                               f"3. {'`Customer Collaboration`':>36} over `Contract Negotiation`\n"
                               f"4. {'`Responding to Change`':>38} over `Following a Plan`\n")


@bot.command(name="urban", help="Return nth urban dictionary definition", aliases=["ubran", "urband"])
async def urban(context, term):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    querystring = {"term": term}

    headers = {
        'x-rapidapi-key': URBAN_API_KEY,
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }

    async with ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as response:
            r = await response.json()
            definition = r['list'][0]['definition']
            print(f"{definition=}")
            embed = discord.Embed(title=term,)
            embed.add_field(name="Definition", value=definition, inline=True)

            await context.channel.send(embed=embed)


if __name__ == "__main__":
    try:
        setup()
        bot.run(TOKEN)
        # client.run(TOKEN)
    except FileNotFoundError:
        logging.error("File was not found, "
                      "are you sure that 'token.txt' exists?")
