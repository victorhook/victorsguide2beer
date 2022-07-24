from dataclasses import asdict
import json
from pathlib import Path
from typing import List

from models import Beer


DATABASE_PATH = Path(__file__).absolute().parent.joinpath('db.json')


class Database:

    @classmethod
    def get_beers(cls) -> List[Beer]:
        beers = []
        for beer in cls._load()['beers']:
            beer = Beer(**beer)
            beers.append(beer)

        return beers

    @classmethod
    def save_beers(cls, beers: List[Beer]) -> None:
        data = cls._load()
        data['beers'] = [asdict(beer) for beer in beers]
        cls._save(data)

    @classmethod
    def _load(cls) -> dict:
        try:
            with open(DATABASE_PATH) as f:
                return json.load(f)
        except FileNotFoundError:
            print(f'Failed to find database at {DATABASE_PATH}'
                  ', creating new one!')
            default_db = {
                'beers': []
            }
            cls._save(default_db)
            return default_db

    @classmethod
    def _save(cls, data: dict) -> None:
        with open(DATABASE_PATH, 'w') as f:
            return json.dump(data, f, indent=4)
