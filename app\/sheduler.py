from apscheduler.schedulers.blocking import BlockingScheduler # pyright: ignore[reportMissingImports]
from utils.backup_supabase import executar_backup # pyright: ignore[reportMissingImports]

sched = BlockingScheduler()
sched.add_job(executar_backup, 'cron', hour=3)
sched.start()
