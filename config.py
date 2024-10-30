import os
from dotenv import load_dotenv
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:

    DB_NAME = os.getenv("DB_NAME", "default_sim_results.db")
    DB_PATH = os.getenv("DB_PATH", os.getcwd())

    @staticmethod
    def get_db_uri():
        return os.path.join(Config.DB_PATH, Config.DB_NAME)

    # Logging Configuration
    LOG_FOLDER = os.environ.get("LOG_FOLDER", "logs")
    LOG_FILE = os.environ.get("LOG_FILE", "app.log")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_MAX_SIZE = int(os.environ.get("LOG_MAX_SIZE", 10 * 1024 * 1024))  # 10 MB
    LOG_BACKUP_COUNT = int(os.environ.get("LOG_BACKUP_COUNT", 5))

    # Derived attributes
    LOG_PATH = os.path.join(LOG_FOLDER, LOG_FILE)
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # Results folder
    RESULTS_FOLDER = os.environ.get("RESULTS_FOLDER", "results")
