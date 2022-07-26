from collections import namedtuple
from dataclasses import dataclass
import os
from pathlib import Path
from typing import List
from flask import Flask, render_template, request
from jinja_markdown import MarkdownExtension

from database import Database as db
import models
import utils


app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)


BASE_PATH = Path(__file__).absolute().parent
POST_PATHS = BASE_PATH.joinpath('templates', 'posts')


@app.route('/')
def get_index():
    events = utils.get_events()
    events = utils.sort_by_date(events)
    new_event_amt = 3

    if len(events) < new_event_amt:
        new_events = events
    else:
        new_events = events[:new_event_amt]

    return render_template(
        'index.html',
        new_events=new_events
    )


class BlogView:

    @app.route('/blog/')
    def get_blog():
        return render_template(
            'blog/blog.html',
            posts=utils.get_posts()
        )

    @app.route('/blog/post/<string:post>')
    def get_post(post: str):
        post_path = f'posts/{post}'
        return render_template(post_path)


@app.route('/brewing/')
def get_brewing():
    return render_template('brewing/brewing.html')


class BeerView:

    @dataclass
    class BeerType:
        beer_type: str
        active: bool = False

        def __hash__(self) -> int:
            return self.beer_type.__hash__()

    @app.route('/beers/')
    def get_beers():
        beer_type = request.args.get('beer_type')
        beers = db.get_beers()
        types = set(BeerView.BeerType(beer.type, False) for beer in beers)


        # Filter by beer type
        if beer_type is not None:
            beers = list(filter(lambda beer: beer.type == beer_type, beers))
            top_three_beers = None
            for beer in types:
                if beer.beer_type == beer_type:
                    beer.active = True
        else:
            sorted_beers = list(reversed(sorted(beers, key=lambda beer: beer.score)))
            if len(sorted_beers) < 3:
                top_three_beers = sorted_beers
            else:
                top_three_beers = sorted_beers[:3]

        return render_template(
            'beer/beers.html',
            beers=beers,
            types=types,
            top_three_beers=top_three_beers
        )

    @app.route('/beers/<string:beer_name>')
    def get_beer(beer_name: str):
        beers = db.get_beers()
        beer_type = request.args.get('beer_type')

        for beer in beers:
            if beer.name == beer_name:
                break

        return render_template(
            'beer/beer.html',
            beer=beer,
        )


'''
Ölsorter:

Topp X lista på landing page
Ölssorter länk till landing page


Månadsgrej:


'''
