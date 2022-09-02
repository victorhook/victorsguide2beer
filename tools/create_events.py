#!/usr/bin/env python3

from copy import copy
from dataclasses import asdict
from datetime import datetime
import json
import pickle
import os
from pathlib import Path
import textwrap
from typing import List
import re
import sys

from markdown import Markdown, markdown

# Add apps to syspath
BASE_PATH = Path(__file__).absolute().parent
APP_PATH = BASE_PATH.parent.joinpath('app')
EVENTS_PATH = APP_PATH.joinpath('events.pickle')
EVENTS_PATH_JSON = APP_PATH.joinpath('events.json')
sys.path.append(str(APP_PATH))

from models import Beer, BlogPost, Event
from database import Database as db


POSTS_PATHS = APP_PATH.joinpath('templates', 'posts')
POST_META_PATH = APP_PATH.joinpath('post_meta.json')

POST_EXCERPT_MAX_LENGTH = 150
AVERAGE_WORDS_PER_MINUTE_READING = 140


def _get_data_in_block(block: str, data: str) -> str:
    regex = '\{%\s*block ' + block + '\s*%\}'
    regex += '\s*(.*?)\s*'
    regex += '{%\s*endblock\s*%}'
    match = re.findall(regex, data, flags=re.DOTALL)
    if match:
        data = match[0]
        data = data.strip()
    else:
        data = None

    return data


def _replace_links_with_text(data: str) -> str:
    # Find all images and remove links completely
    cleaned_data = re.sub('\!\[(.*)\]\(.*\)', '', data)

    repl = {}
    for link in re.finditer('\[(.*?)\]\(.*\)', copy(cleaned_data)):
        link_name = link.group(1)
        link_full = cleaned_data[link.start():link.end()]
        repl[link_full] = link_name

    for link_full, link_name in repl.items():
        cleaned_data = cleaned_data.replace(link_full, link_name)

    return cleaned_data


def create_posts() -> List[BlogPost]:
    posts = []

    for post in os.listdir(str(POSTS_PATHS)):
        abs_path = POSTS_PATHS.joinpath(post)

        post_title = ''
        post_date = ''
        post_image = ''
        post_excerpt = ''
        post_image_translate_y = ''
        post_read_length = 0

        with open(abs_path, encoding='utf-8') as f:
            data = f.read()
            post_title = _get_data_in_block('post_title', data)
            post_date = _get_data_in_block('post_date', data)
            post_image = _get_data_in_block('post_image', data)
            post_image_translate_y = _get_data_in_block('post_image_translate_y', data)
            post_body = _get_data_in_block('post_body', data)

        post_body_only_text = _replace_links_with_text(post_body)

        # Get pots excerpt.
        if len(post_body_only_text) > POST_EXCERPT_MAX_LENGTH:
            post_excerpt = post_body_only_text[:POST_EXCERPT_MAX_LENGTH]
        else:
            post_excerpt = post_body_only_text

        if post_excerpt:
            if post_excerpt[-1] != ' ':
                post_excerpt += ' '
            post_excerpt += '...'
            post_excerpt = textwrap.dedent(post_excerpt)

        # TODO: Fix better solution for this
        if post_image is not None:
            post_image = '/static/images/posts/' + post_image

        post_read_length = len(post_body_only_text.split(' ')) // AVERAGE_WORDS_PER_MINUTE_READING

        blog_post = BlogPost(
            post_date,
            post_title,
            post_excerpt,
            post_read_length,
            post_image,
            post_image_translate_y,
            post
        )

        posts.append(blog_post)

    return posts


def get_events() -> List[Event]:
    beers = db.get_beers()
    posts = create_posts()
    events = []
    for beer in beers:
        events.append(Event(beer.added_date, beer))
    for post in posts:
        events.append(Event(post.date, post))
    return events


def sort_by_date(events: List[Event]) -> List[Event]:
    def sorter(event: Event):
        return datetime.strptime(event.added_date, '%Y-%m-%d')

    return list(sorted(events, key=sorter))


if __name__ == '__main__':
    posts = create_posts()
    beers = db.get_beers()
    events = posts + beers
    print(f'Saving events to {EVENTS_PATH} and json to {EVENTS_PATH_JSON}')
    with open(EVENTS_PATH, 'wb') as f:
        pickle.dump(events, f)

    def jsonify_event(event: Event) -> dict:
        event_json = asdict(event)
        event_json['type'] = event.__class__.__name__
        return event_json

    with open(EVENTS_PATH_JSON, 'w') as f:
        data = [jsonify_event(event) for event in events]
        json.dump(data, f, indent=4)