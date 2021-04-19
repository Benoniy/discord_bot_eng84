import random
import group_picker
from bot import is_authorized


async def check_args(message, args, amount):
    try:
        a = args[amount]
        return True
    except IndexError:
        await message.channel.send(f"Error this command requires {amount} arguments")
        return False


async def clear(message):
    await message.channel.send(".\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n."
                               "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n.")


async def group_pick(message, args):
    if await check_args(message, args, 1):
        members = args[1]
        if members.isdigit():
            members = int(members)
            if members > 0:
                await message.channel.send(group_picker.split_list(members))
            else:
                await message.channel.send("Please enter an argument that is greater than 0!")
        else:
            await message.channel.send("Please enter an argument that is a number!")


async def bot_help(message):
    """ Provides a list of commands to the user """
    await message.channel.send("`}help` - For obvious reasons.\n"
                               "`}clear` - Used to clear the page so that we don't get in trouble.\n"
                               "`}groups x` - Used to create groups of x many people.\n"
                               "`}roll x y` - Used to roll x many y sized dice.\n"
                               "`}flip_coin` - Returns heads or tails.\n"
                               )


async def roll_dice(message, args):
    """ Rolls a specified number of user defined dice """

    if await check_args(message, args, 2):
        to_send = ""

        if args[1].isdigit() and args[2].isdigit():
            # Send values specified in message to int
            no_dice = int(args[1])
            no_sides = int(args[2])

            if no_dice > 20:
                no_dice = 20

            if no_sides > 120:
                no_sides = 120

            # Check size - avoid excess calculation
            if no_dice > 10:
                no_dice = 10
            if no_sides > 100:
                no_sides = 100

            # Run dice-rolls
            for die in range(no_dice):
                roll = random.randint(1, no_sides)
                to_send += "{0},\n".format(roll)

            to_send = to_send[:-2]
            # Send Message
            await message.channel.send(to_send)
        else:
            await message.channel.send("Both of your arguments should be numbers!")


async def flip_coin(message):
    """ Flips a coin and displays the result """
    to_send = ""
    flip = bool(random.getrandbits(1))

    if flip:
        to_send += "Heads!"
    else:
        to_send += "Tails!"

    await message.channel.send(to_send)
