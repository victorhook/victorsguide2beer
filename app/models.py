from typing import Union
from dataclasses import dataclass


@dataclass
class BlogPost:
    title: str
    date: str
    excerpt: str
    path: str


@dataclass
class Beer:
    name: str
    country: str
    type: str
    alcohol: float
    score: int
    added_date: str
    year: str = ''
    image: str = None
    brewery: str = ''
    description: str = ''



@dataclass
class Event:
    added_date: str
    event: Union[Beer, BlogPost]
