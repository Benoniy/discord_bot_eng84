import random

eng84_members = ["Andrew",
                 "Arun",
                 "Alexis",
                 "Ben",
                 "Dunni",
                 "Isobel",
                 "Jordan",
                 "Jose",
                 "Oleg",
                 "Saverio",
                 "William",
                 "Ula"
                ]


def group_items(members, group_by):
    """
    Return members as a list of lists according to their shuffled groups.

    The function tries to group the members according to the 'group_by' number.
    If it is not divisible by number of members, the number of teams will be rounded up or down according to round() function

    INPUTS
    members: the list of members or list of items
    group_by: the number of which the function should group the items by

    OUTPUTS
    groups: list groups. Each group is a list with the names of item/member in the members list

    e.g
    """
    # Get member number
    original_members = members
    membernum = len(members)
    # Create a list of indices for each member (also uncouple from original list)
    members = list(range(membernum))
    # Decide on number of teams
    teamnum = round(membernum / group_by)
    # Get quotient and remainder from division of new team number
    quotient, remainder = divmod(membernum, teamnum)
    # Shuffle members of team
    random.shuffle(members)
    groups = []
    stop = 0
    for i in range(1, teamnum+1):
        start = stop
        # Find if quotient +1 or just quotient members are put in team
        stop += quotient + 1 if i <= remainder else quotient
        # Use list of member indices as mask to get the names of original members
        groups.append(list(map(original_members.__getitem__, members[start:stop])))

    return groups


def display_groups(groups):
    message = ""
    for idx, group in enumerate(groups, 1):
        message += f"Team {idx}: {', '.join(group)}\n"

    return message


def gen_groups(size):
    groups = group_items(eng84_members.copy(), size)
    return display_groups(groups)


# showcase function
if __name__ == "__main__":
    print(gen_groups(3))
