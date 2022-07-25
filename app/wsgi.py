from pathlib import Path
import sys


# SKIP THIS when running apache: if __name__ == '__main__':

BASE_PATH = Path(__file__).absolute().parent
sys.path.append(str(BASE_PATH))
sys.path.append(str(BASE_PATH.parent))

# We just import the application, do not run it, if using apache!
from app.main import app as application
