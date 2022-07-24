import os
from pathlib import Path
import textwrap
from typing import List

from models import Beer, BlogPost


POST_EXCERPT_MAX_LENGTH = 50


def get_posts(post_path: Path) -> List[BlogPost]:
    posts = []

    for post in os.listdir(str(post_path)):
        abs_path = post_path.joinpath(post)

        got_all = False
        post_title = ''
        post_date = ''
        post_excerpt = ''

        with open(abs_path) as f:
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



if __name__ == '__main__':
    POST_PATHS = Path('/home/victor/coding/projects/hookbeer/app/templates/posts')
    #print(get_posts(POST_PATHS))    
    from database import Database as db
    #Database.save_beers([Beer('testbere', 'Germany', 'Weissbeer')])
    beers = db.get_beers()
    #beers.append(Beer('test2', 'Sweden', 'Golden blonde'))
    #db.save_beers(beers)
