import random

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

members = orig_members.copy()


def split_list(mem_count):
    global members
    """ Uses RNG to pick members for each teams """
    team_no = 1
    count = 0
    full_str = ""
    string = ""

    for _ in range(0, len(members), 1):
        rand = random.randint(0, len(members) - 1)
        string += members[rand]
        members.pop(rand)
        count += 1
        if count == mem_count:
            if len(members) < mem_count:
                string += ", " + members[0]
                members.pop(0)
            full_str += f"Team {team_no}: {string}\n"

            string = ""
            count = 0
            team_no += 1

        else:
            string += ", "

        if len(members) == 0:
            break
    # If teams are uneven in numbers then print the uneven team
    if string:
        full_str += f"Team {team_no}: {string[:-2]}"

    members = orig_members.copy()
    return full_str
