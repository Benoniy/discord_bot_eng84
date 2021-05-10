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

import group_picker
import scheduling

# import bot_commands


logging.basicConfig(filename="log.txt", level=logging.DEBUG, filemode="w")

# Global Variables
# client = discord.Client()
TOKEN = ""
BOT_PREFIX = "+"
URBAN_API_KEY = ""

bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)
bot.remove_command('help')


def setup():
    """ Get token & prefix from file and assigns to variables """
    with open("tokens.yaml") as stream:

        global TOKEN
        global BOT_PREFIX
        global URBAN_API_KEY
        file = open("token.txt", "r")
        TOKEN = file.readline().replace("\n", "")
        BOT_PREFIX = file.readline().replace("\n", "")
        URBAN_API_KEY = file.readline().replace("\n", "")
        file.close()
        logging.info(f"Bot token '{TOKEN}' and prefix '{BOT_PREFIX}' are set")


@bot.event
async def on_ready():
    """ Set Discord Status """
    logging.info("Bot is Ready")
    print("Bot is Ready")
    await bot.change_presence(activity=discord.Activity(
                                 type=discord.ActivityType.listening,
                                 name=BOT_PREFIX + "commands"))


@bot.command(name='clear', help='Used to clear the page for x minutes')
async def clear(context, minutes=1):
    """ Sending large message to clear screen temporarily """
    message = await context.channel.send(
            ".\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n."
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n."
            )
    # Waiting time in minutes
    await asyncio.sleep(minutes * 60)
    # Delete message after wait
    await message.delete()


@bot.command(name='groups', help='Try to create groups of x many people. Default to groups of 2')
async def groups(context, *, number_of_people=2):
    """ Pick groups """
    if number_of_people < 1:
        await context.channel.send('Number of people in groups must be above 0')
    else:
        await context.channel.send(group_picker.gen_groups(number_of_people))


class NumberWithThreshold(commands.Converter):
    async def convert(self, context, argument, threshold=100):
        argument = int(argument)
        return argument if argument <= threshold else threshold


class SidesNumber(NumberWithThreshold):
    async def convert(self, *args):
        return await super().convert(*args, threshold=120)


class DiceNumber(NumberWithThreshold):
    async def convert(self, *args):
        return await super().convert(*args, threshold=20)


@bot.command(name='roll', help="Roll's x number of y sided dice.", aliases=["rol"])
async def roll_dice(context, x=1, y=6):
    """ Rolls a specified number of user defined dice

        If x or y is not a digit, it will take the default value of 1 and 6 respectively
        Additionally, sides and dice have max values of 120 and 20. If the input surpasses the
        max values, they automatically get assigned their max value

    """

    # Round and clamp values
    x = round(max(min(20, x), 1))
    y = round(max(min(120, y), 1))
    # print(x, y)
    if x > 0 and y > 0:

        to_send = "Rolled:\n"
        for die in range(x):
            roll = random.randint(1, y)
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

    await context.channel.send(to_send)


@bot.command(name="agile", help="List agile values")
async def agile(context):
    await context.channel.send("Whilst there is value to the items on the right, we should value items on the left more!\n" +
                               "1. {rule:>30} over `Processes and Tools`\n".format(rule='`Individuals and Interactions`') +
                               "2. {rule:>42} over `Comprehensive Documentation`\n".format(rule='`Working Software`') +
                               "3. {rule:>36} over `Contract Negotiation`\n".format(rule='`Customer Collaboration`') +
                               "4. {rule:>38} over `Following a Plan`\n".format(rule='`Responding to Change`'))


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
            print(definition + "=")
            embed = discord.Embed(title=term,)
            embed.add_field(name="Definition", value=definition, inline=True)

            await context.channel.send(embed=embed)


@bot.group(name="schedule", help="Show schedule", invoke_without_command=True, aliases=['scedule', 'shedule', 'shcedule'])
async def schedule(context):
    sch = scheduling.Week()
    await context.channel.send(sch.get_schedule())


@schedule.command(name='get')
async def schedule_get(context, *, args: str):
    sch = scheduling.Week()
    to_send = sch.get_time(args.lower())
    if to_send is not None:
        await context.channel.send(to_send)
    else:
        await context.channel.send("Invalid input")


@schedule.command(name='set')
async def schedule_set(context):
    await context.channel.send('Setting day')


@bot.command(name="help")
async def help(context):
    """ Provides a list of commands to the user """
    await context.channel.send(f"\n"
                               "• `" + BOT_PREFIX + "help     ` - For obvious reasons.\n"
                               "• `" + BOT_PREFIX + "clear x  ` - Used to clear the page for x many minutes so that we don't get in trouble.\n"
                               "• `" + BOT_PREFIX + "groups x ` - Used to create groups of x many people.\n"
                               "• `" + BOT_PREFIX + "roll x y ` - Used to roll x many y sized dice.\n"
                               "• `" + BOT_PREFIX + "flip_coin` - Returns heads or tails.\n"
                               "• `" + BOT_PREFIX + "agile    ` - Lists the four values of agile\n"
                               "• `" + BOT_PREFIX + "schedule ` - Shows the schedule\n"
                               "• `" + BOT_PREFIX + "urban x  ` - Gets the urban dictionary definition of x"
                               "\n"
                               )

if __name__ == "__main__":
    try:
        setup()
        bot.run(TOKEN)
        # client.run(TOKEN)
    except FileNotFoundError:
        logging.error("File was not found, "
                      "are you sure that 'token.txt' exists?")
