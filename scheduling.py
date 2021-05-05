import datetime
import calendar
from typing import Optional, Sequence


DAYS = {
        **dict.fromkeys(['m', 'mon', 'monday'], 0),
        **dict.fromkeys(['tu', 'tue', 'tuesday'], 1),
        **dict.fromkeys(['w', 'wed', 'wednesday'], 2),
        **dict.fromkeys(['th', 'thu', 'thursday'], 3),
        **dict.fromkeys(['f', 'fri', 'friday'], 4),
        **dict.fromkeys(['sa', 'sat', 'saturday'], 5),
        **dict.fromkeys(['su', 'sun', 'sunday'], 6),
        }


class Week:
    standup_times = {
            0: '9:30',
            1: '9:00',
            2: '9:30',
            3: '9:00',
            4: '9:30',
            5: None,
            6: None,
            }

    def get_time(self, arg: Optional[str]):

        day_num = DAYS.get(arg)
        if day_num is not None:
            return f'Standup at {self.standup_times[day_num]}'


    def set_time(self, arg: str, time: str):
        pass

    def get_schedule(self):
        training_week = datetime.datetime.now().isocalendar()[1]
        return f'Week {training_week}:\n' + '\n'.join([f'{calendar.day_name[day]}  \t {time}' for day, time in self.standup_times.items() if time is not None])
