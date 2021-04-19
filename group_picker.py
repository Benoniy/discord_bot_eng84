import random

test_members = [
        "A1", "A2", "A3", "A4", "A5",
        "B1", "B2", "B3", "B4", "B5",
        "C1", "C2", "C3", "C4", "C5",
        "D1", "D2", "D3", "D4", "D5",
        "E1", "E2", "E3", "E4", "E5",
        "F1", "F2", "F3", "F4", "F5",
        "G1", "G2", "G3", "G4", "G5",
        "H1", "H2", "H3", "H4", "H5",
        "I1", "I2", "I3", "I4", "I5",
        "J1", "J2", "J3", "J4", "J5",
        "K1", "K2", "K3", "K4", "K5",
        "L1", "L2", "L3", "L4", "L5",
        "M1", "M2", "M3", "M4", "M5",
        "N1", "N2", "N3", "N4", "N5",
        "O1", "O2", "O3", "O4", "O5",
        ]

orig_members = ["Andrew",
                "Arun",
                "Alexis",
                "Ben",
                "Beth",
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

def split_list(group_by):
    return display_groups(group_items(orig_members, group_by))

# showcase function
if __name__ == "__main__":

    # TEST 1
    members = test_members
    groups = group_items(members, 7)
    print('Initial members list:')
    print(members)
    print('Groups:')
    print(display_groups(groups))

    # TEST 2
    # members = orig_members
    # groups = group_items(members, 3)
    # print('Initial members list:')
    # print(members)
    # print('Groups:')
    # print(display_groups(groups))

    # TEST 3
    # print(split_list(3))


