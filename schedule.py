import datetime

class Day:

    def __init__(name: str, standup: datetime.time):
        self.name = name
        self.standup = standup


class Week:
    monday = Day('Monday') 
