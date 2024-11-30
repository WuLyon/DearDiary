from pathlib import Path
import logging.config

USER_NAME = 'Lyon'
USER_ID = '0001'

logger = logging.getLogger(__name__)

APP_PATH = Path(__file__).resolve().parent

LYON_SUBJECT = [
    'Python',
    'Math',
    'English',
    'Exercise',
    'Reading',
    'Paint',
    'Hygiene',
    'Cardistry',
    'Film',
    'Music',
    'Meditation',
    'Nosex',
    'Sleep'
]
DEFAULT_SUBJECT = [
    'Exercise',
    'Reading',
    'Sleep'
]

def test():
    logger.info(f"Have set configuration APP_PATH: {APP_PATH}")