from dataclasses import dataclass, field


@dataclass
class Event:
    date: str

    def event_type(self) -> None:
        return self.__class__.__name__


@dataclass
class BlogPost(Event):
    title: str
    excerpt: str
    read_length: int
    image: str
    translate_image_y: str
    path: str


@dataclass
class Beer(Event):
    name: str
    country: str
    type: str
    alcohol: float
    score: int
    year: str = ''
    image: str = None
    brewery: str = ''
    description: str = ''
