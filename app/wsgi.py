from pathlib import Path
import sys
from app.main import app


if __name__ == '__main__':
    BASE_PATH = Path(__file__).absolute().parent
    sys.path.append(str(BASE_PATH))

    from app import app
