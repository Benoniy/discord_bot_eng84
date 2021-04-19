import random
import group_picker
from bot import is_authorized


async def clear(message):
    await message.channel.send(".\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n."
                               "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n.")


async def group_pick(message, members):
    await message.channel.send(group_picker.split_list(members))


async def bot_help(message):
    """ Provides a list of commands to the user """
    await message.channel.send("`}clear` - used to clear the page so that we don't get in trouble.\n"
                               "`}groups x` - Used to create groups of x many people.\n"
                               )


async def roll_dice(message, args):
    """ Rolls a specified number of user defined dice """
    to_send = ""

    try:
        # Send values specified in message to int
        no_dice = int(args[1])
        no_sides = int(args[2])

        # Check size - avoid excess calculation
        if no_dice > 10:
            no_dice = 10
        if no_sides > 100:
            no_sides = 100

        # Run dice-rolls
        for die in range(no_dice):
            roll = random.randint(1, no_sides)
            to_send += "{0}, ".format(roll)

        # Send Message
        await message.channel.send(to_send)

    except ValueError:
        await message.channel.send("**Error:** }roll should have 2 arguments!")


async def flip_coin(message):
    """ Flips a coin and displays the result """
    to_send = ""
    flip = bool(random.getrandbits(1))

    if flip:
        to_send += "Heads!"
    else:
        to_send += "Tails!"

    await message.channel.send(to_send)
