import telegram, logging, os, datetime

import modules.pytg.managers.data_manager as data_manager
import modules.pytg.managers.config_manager as config_manager

from modules.dmibot.utils.lessons_utils import *

def scrape_lessons_job(context):
    logging.info("Running scrape lessons job...")

    scrape_lessons()