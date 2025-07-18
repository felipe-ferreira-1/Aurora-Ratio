from apscheduler.schedulers.blocking import BlockingScheduler
from utils.backup_supabase import executar_backup

sched = BlockingScheduler()
sched.add_job(executar_backup, 'cron', hour=3)
sched.start()
