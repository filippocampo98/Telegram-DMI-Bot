import telegram, logging, os, datetime

import modules.pytg.managers.data_manager as data_manager
import modules.pytg.managers.config_manager as config_manager

from modules.dmibot.utils.exams_utils import *

def scrape_exams_job(context):
    logging.info("Running scrape exams job...")

    scrape_exams()