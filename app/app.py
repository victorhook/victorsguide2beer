from collections import namedtuple
from dataclasses import dataclass, fields
import os
from pathlib import Path
from typing import List
from flask import Flask, render_template, request, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from jinja_markdown import MarkdownExtension
from datetime import datetime

from database import Database as db
import models
import utils


app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

BASE_PATH = Path(__file__).absolute().parent
POST_PATHS = BASE_PATH.joinpath('templates', 'posts')

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


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
        posts = utils.get_posts()
        posts = utils.sort_by_date(posts)
        return render_template(
            'blog/blog.html',
            posts=posts
        )

    @app.route('/blog/post/<string:post>')
    def get_post(post: str):
        post_path = f'posts/{post}'
        return render_template(post_path)


class BrewingView:

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

    @classmethod
    def _remove_nones(cls, beer: models.Beer) -> models.Beer:
        if not beer.year:
            beer.year = 'Oklart'
        if not beer.brewery:
            beer.brewery = 'Oklart'
        #if not beer.description:
        #    beer.description = 'Ingen utförlig beskrivning är skriven om' + \
        #                        f' {beer.name} än.'
        return beer

    @app.route('/beers/')
    def get_beers():
        beer_type = request.args.get('beer_type')
        beers = db.get_beers()
        beers = list(map(BeerView._remove_nones, beers))
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
        beers = list(map(BeerView._remove_nones, beers))
        beer_type = request.args.get('beer_type')

        for beer in beers:
            if beer.name == beer_name:
                break

        return render_template(
            'beer/beer.html',
            beer=beer,
        )


# --- Filters --- #
@app.template_filter()
def post_image(image: str) -> str:
    # TODO: Better solution for this?
    pre = '/static/images/posts/'
    return pre + image.strip()

@app.template_filter()
def beer_image(image: str) -> str:
    # TODO: Better solution for this?
    pre = '/static/beers/'
    return pre + image.strip()

@app.template_filter()
def ref(number: int, author: str, title: str, date: str, url: str) -> str:
    return '<p class="ref">' + f'{number}. {author}. {title}. {date}: {url}' + '</p>'


class Admin:

    @app.route('/add_beer')
    @auth.login_required
    def add_beer() -> None:
        return render_template(
            'admin/admin.html'
        )

    @app.route('/add_new_beer', methods=['POST'])
    @auth.login_required
    def add_new_beer() -> None:
        date = datetime.now().strftime('%Y-%m-%d')
        new_beer = models.Beer(**request.form, date=date)
        new_beer.score = float(new_beer.score)
        new_beer.alcohol = float(new_beer.alcohol)

        image = request.files['image']

        BEER_RELPATH = Path('static/beers')
        relpath = BEER_RELPATH.joinpath(image.filename)

        # Save to absolute path
        abspath = str(BASE_PATH.joinpath(relpath))
        image.save(abspath)
        new_beer.image = str(relpath)
        if not new_beer.image.startswith('/'):
            new_beer.image = '/' + new_beer.image

        beers = db.get_beers()
        beers.append(new_beer)
        db.save_beers(beers)

        return render_template(
            'admin/admin.html'
        )


'''
Ölsorter:

Topp X lista på landing page
Ölssorter länk till landing page


Månadsgrej:


'''
