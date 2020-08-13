import os
import re
import logging
from datetime import datetime
from dateutil import tz
from todoist.api import TodoistAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TODOIST_DATE_FORMAT = "%Y-%m-%d"


def get_token():
    token = os.getenv('TODOIST_APIKEY')
    if not token:
        raise Exception('Please set the API token in environment variable.')
    return token


class Task(object):
    def __init__(self, item):
        self.item = item

    def get_habit(self):
        #Update: [day 'streak'/'habit_goal(in days)']
        return re.search(r'\[day\s(\d+)\/(\d+)]', self.item['content'])

    def is_habit(self):
        """
        Check if task is a habit task.
        """
        habit = self.get_habit()
        conditions = [
            habit,  # Task has to be a habit pattern
            self.item['due'].get('date') if self.item['due'] else None,  # Task has to have due date
            not self.item['in_history']  # Task should not be archived
        ]
        return all(conditions)

    @property
    def due_date(self):
        """
        Get the due date for the current task.
        :return:
        """
        return self.item['due'].get('date')

    def is_due(self, today):
        """
        Check if task is due.
        """
        return self.due_date != today

    @property
    def current_streak(self):
        """
        Parse and get current stream from the pattern.

        Pattern: [day X]
        :return: Current streak
        """
        habit = self.get_habit()
        return int(habit.group(1))

    @property
    def current_goal(self):
        """
        Parse and get current goal to develop a habit in days from the pattern.

        Pattern: [day X/G]
        :return: Goal streak
        """
        habit = self.get_habit()
        return int(habit.group(2))

    def set_streak(self, streak, goal):
        """
        Set streak for a task.
        :param streak: Number of days
        :param goal: Habit goal in days
        :return: None
        """
        days = '[day {}/{}]'.format(streak,goal)
        text = re.sub(r'\[day\s(\d+)\/(\d+)]', days, self.item['content'])
        self.item.update(content=text)

    def increase(self, n=1):
        """
        Increase streak by n days.
        Default: 1 day
        :param n: Number of days
        """
        self.set_streak(self.current_streak + n,self.current_goal)

    def decrease(self, today):
        """
        Decrease streak by 1 day.
        Doesn't go to negative.
        """
        streak = max(0, self.current_streak - 1)
        self.set_streak(streak,self.current_goal)
        self.item.update(due={'string': 'ev day starting {}'.format(today)})

    def reset_to_zero(self, today):
        """
        Set streak to zero.
        """
        self.set_streak(0,self.current_goal)
        self.item.update(due={'string': 'ev day starting {}'.format(today)})

    def habbit_complete(self):
        """
        returns True is streak == goal.
        """
        if self.current_streak >= self.current_goal:
            return True
        return False

    def delete_task(self):
        """
        Delete task if goal is completed
        """
        self.item.delete()
        
class Todoist(object):
    def __init__(self):
        self.api = TodoistAPI(get_token())
        self.api.sync()

    @property
    def today(self):
        timezone = self.api.state['user']['tz_info']['timezone']
        tz_location = tz.gettz(timezone)
        now = datetime.now(tz=tz_location)
        return now.strftime(TODOIST_DATE_FORMAT)

    def update_streak(self):
        items = self.api.state['items']
        for item in items:
            task = Task(item)
            if task.is_habit():
                if task.is_due(self.today):
                    task.reset_to_zero(self.today)
                else:
                    task.increase()
                    if task.habbit_complete():
                        task.delete_task()
        self.api.commit()


def main():
    todo = Todoist()
    todo.update_streak()


if __name__ == '__main__':
    main()
