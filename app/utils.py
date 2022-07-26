from datetime import datetime
import os
from pathlib import Path
import textwrap
from typing import List

from models import Beer, BlogPost, Event
from database import Database as db


BASE_PATH = Path(__file__).absolute().parent
POSTS_PATHS = BASE_PATH.joinpath('templates', 'posts')

POST_EXCERPT_MAX_LENGTH = 50


def get_posts() -> List[BlogPost]:
    posts = []

    for post in os.listdir(str(POSTS_PATHS)):
        abs_path = POSTS_PATHS.joinpath(post)

        got_all = False
        post_title = ''
        post_date = ''
        post_excerpt = ''

        with open(abs_path, encoding='utf-8') as f:
            while not got_all and (f.tell() < abs_path.stat().st_size):
                line = f.readline()

                if 'block post_title' in line:
                    line = f.readline()
                    while not 'endblock' in line:
                        post_title += line
                        line = f.readline()

                elif 'block post_date' in line:
                    line = f.readline()
                    while not 'endblock' in line:
                        post_date += line
                        line = f.readline()

                elif 'block post_body' in line:
                    line = f.readline()
                    while not 'endblock' in line and len(post_excerpt) < POST_EXCERPT_MAX_LENGTH:
                        post_excerpt += line
                        line = f.readline()
                    got_all = True

        post_title = post_title.strip()
        post_date = post_date.strip()

        if len(post_excerpt) > POST_EXCERPT_MAX_LENGTH:
            post_excerpt = post_excerpt[:POST_EXCERPT_MAX_LENGTH]
        post_excerpt = textwrap.dedent(post_excerpt).strip()

        blog_post = BlogPost(post_title, post_date, post_excerpt, post)
        posts.append(blog_post)

    return posts


def sort_by_date(events: List[Event]) -> List[Event]:
    def sorter(event: Event):
        return datetime.strptime(event.added_date, '%Y-%m-%d')

    return list(sorted(events, key=sorter))


def get_events() -> List[Event]:
    beers = db.get_beers()
    posts = get_posts()
    events = []
    for beer in beers:
        events.append(Event(beer.added_date, beer))
    for post in posts:
        events.append(Event(post.date, post))
    return events


if __name__ == '__main__':
    #print(get_posts(POST_PATHS))    
    #from database import Database as db
    #Database.save_beers([Beer('testbere', 'Germany', 'Weissbeer')])
    #beers = db.get_beers()
    #beers.append(Beer('test2', 'Sweden', 'Golden blonde'))
    #db.save_beers(beers)
    print(get_events())
