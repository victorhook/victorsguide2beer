from copy import copy
from datetime import datetime
import os
from pathlib import Path
import pickle
from typing import List


from models import Beer, BlogPost, Event
from database import Database as db


BASE_PATH = Path(__file__).absolute().parent
POSTS_PATHS = BASE_PATH.joinpath('templates', 'posts')
EVENTS_PATH = BASE_PATH.joinpath('events.pickle')



def date() -> str:
    return datetime.now().strftime('%Y-%m-%d')


def sort_by_date(events: List[Event]) -> List[Event]:
    def sorter(event: Event):
        return datetime.strptime(event.date, '%Y-%m-%d')

    return list(reversed(sorted(events, key=sorter)))


def get_posts() -> List[BlogPost]:
    events = get_events()
    return list(filter(lambda e: e.event_type() == 'BlogPost', events))


def get_events() -> List[Event]:
    with open(EVENTS_PATH, 'rb') as f:
        events = pickle.load(f)

    return events

if __name__ == '__main__':
    get_posts()
