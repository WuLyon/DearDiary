from pathlib import Path
import logging.config


logger = logging.getLogger(__name__)

APP_PATH = Path(__file__).resolve().parent

def test():
    logger.info(f"Have set configuration APP_PATH: {APP_PATH}")