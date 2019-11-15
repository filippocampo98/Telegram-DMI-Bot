import telegram, yaml, logging

from modules.dmibot.handlers.jobs.scrape_exams import scrape_exams_job

def schedule_jobs(job_queue):
    job_queue.run_repeating(scrape_exams_job, interval=24*60*60)
