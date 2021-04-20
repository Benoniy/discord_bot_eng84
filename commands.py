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


async def agile(message):
    await message.channel.send("Whilst there is value to the items on the right, we should value items on the left more!\n"
                               f"1. {'`Individuals and Interactions`':>30} over `Processes and Tools`\n"
                               f"2. {'`Working Software`':>42} over `Comprehensive Documentation`\n"
                               f"3. {'`Customer Collaboration`':>36} over `Contract Negotiation`\n"
                               f"4. {'`Responding to Change`':>38} over `Following a Plan`\n")


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


async def bot_help(message, prefix):
    """ Provides a list of commands to the user """
    await message.channel.send(f"`{prefix}help` - For obvious reasons.\n"
                               f"`{prefix}clear` - Used to clear the page so that we don't get in trouble.\n"
                               f"`{prefix}groups x` - Used to create groups of x many people.\n"
                               f"`{prefix}roll x y` - Used to roll x many y sized dice.\n"
                               f"`{prefix}flip_coin` - Returns heads or tails.\n"
                               f"`{prefix}agile` - Lists the four values of agile"
                               )


async def roll_dice(message, args):
    """ Rolls a specified number of user defined dice """

    if await check_args(message, args, 2):
        to_send = ""

        if args[1].isdigit() and args[2].isdigit():
            # Send values specified in message to int
            no_dice = int(args[1])
            no_sides = int(args[2])

            # Check size - avoid excess calculation
            if no_dice > 20:
                no_dice = 20

            if no_sides > 120:
                no_sides = 120

            # Run dice-role's
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
