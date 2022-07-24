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
    score: int
    year: str = ''
    image: str = None
    brewery: str = ''
    description: str = ''
