# BasicBot
# Code lifted from StockImage bot by meed223 with other minor contributors

import logging
import discord
from regex import regex
import commands


logging.basicConfig(filename="log.txt", level=logging.DEBUG, filemode="w")

# Global Variables
client = discord.Client()
TOKEN = ""
BOT_PREFIX = ""


def setup():
    """ Get token & prefix from file and assigns to variables """
    file = open("token.txt", "r")
    global TOKEN
    TOKEN = file.readline().replace("\n", "")

    global BOT_PREFIX
    BOT_PREFIX = file.readline().replace("\n", "")
    file.close()
    logging.info(f"Bot token '{TOKEN}' and prefix '{BOT_PREFIX}' are set")


# ---[ Bot Event Code ]---
@client.event
async def on_ready():
    """ Set Discord Status """
    logging.info("Bot is Ready")
    print("Bot is Ready")
    await client.change_presence(activity=discord.Activity(
                                 type=discord.ActivityType.listening,
                                 name=f"{BOT_PREFIX}commands"))


@client.event
async def on_member_join(member):
    """  New member joined server """
    print("member joined")


@client.event
async def on_guild_join(guild):
    """  Joined a new server """
    print("bot joined")


@client.event
async def on_message(message):
    """  This is run when a message is received on any channel """
    author = message.author
    o_args = message.content.strip().lower().split(' ')

    if author != client.user and BOT_PREFIX == o_args[0][0]:
        o_args[0] = o_args[0].replace(BOT_PREFIX, "")
        args = []

        for arg in o_args:
            if regex.search("[A-Z]+|[a-z]+|\d+", arg):
                args.append(arg)

        if args[0] == "clear":
            await commands.clear(message)
        elif args[0] == "groups":
            await commands.group_pick(message, args)
        elif args[0] == "help":
            await commands.bot_help(message, BOT_PREFIX)
        elif args[0] == "flip_coin":
            await commands.flip_coin(message)
        elif args[0] == "roll":
            await commands.roll_dice(message, args)
        elif args[0] == "agile":
            await commands.agile(message)
        else:
            await message.channel.send(f"Command not recognised, use {BOT_PREFIX}help to see all available commands!")


def is_authorized(message):
    """  Checks user privileges """
    authorized = False
    for member in message.guild.members:
        if member.id == message.author.id:
            # Check this ID specifically
            for r in member.roles:
                if r.permissions.manage_guild:
                    authorized = True
                    break
    return authorized


if __name__ == "__main__":
    try:
        setup()
        client.run(TOKEN)
    except FileNotFoundError:
        logging.error("File was not found, "
                      "are you sure that 'token.txt' exists?")
