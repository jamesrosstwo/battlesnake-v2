from apscheduler.schedulers.blocking import BlockingScheduler

from agent.model.data_generator.__main__ import scrape_pruzze

scrape_pruzze()
scheduler = BlockingScheduler()
scheduler.add_job(scrape_pruzze, 'interval', hours=1)
scheduler.start()