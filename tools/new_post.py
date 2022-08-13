#!/usr/bin/env python3

BASE_POST = """\
{{% extends 'blog/post.html' %}}

{{% block post_title %}}
    {title}
{{% endblock %}}

{{% block post_date %}}
    {date}
{{% endblock %}}

{{% block post_body %}}
{{% endblock %}}


{{% block post_references %}}
    {{{{ utils.ref(1, "La Trappe", "Our Trappist Ales", "08-08-2022", "https://uk.latrappetrappist.com/gb/en/products.html") }}}}
{{% endblock %}}
"""

from datetime import datetime
from pathlib import Path
import os
import sys


BASE_PATH = Path(__file__).absolute().parent.parent
POST_PATH = BASE_PATH.joinpath('app', 'templates', 'posts')


def save_file(title: str) -> None:
    date = datetime.now().strftime('%Y-%m-%d')
    filename = date + '_' + title.replace(' ', '_')
    filepath = POST_PATH.joinpath(filename)
    filepath = str(filepath) + '.html'

    if os.path.exists(filepath):
        print(f'Error. Filepath "{filepath}" already exists.')
        sys.exit(0)

    data = BASE_POST.format(title=title, date=date)
    print(f'Creating new post {filename} to path: "{filepath}"')
    with open(filepath, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    title = input('Title: ')
    save_file(title)
