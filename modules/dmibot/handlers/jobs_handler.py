import telegram, yaml, logging

from modules.dmibot.handlers.jobs.scrape_exams import scrape_exams_job
from modules.dmibot.handlers.jobs.scrape_lessons import scrape_lessons_job
from modules.dmibot.handlers.jobs.scrape_professors import scrape_professors_job

def schedule_jobs(job_queue):
    job_queue.run_repeating(scrape_exams_job, interval=24*60*60)
    job_queue.run_repeating(scrape_lessons_job, interval=24*60*60)
    job_queue.run_repeating(scrape_professors_job, interval=24*60*60)
