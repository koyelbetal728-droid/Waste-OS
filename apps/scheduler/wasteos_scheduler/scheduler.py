"""Real interval-based scheduler loop — no APScheduler dependency needed
for this scaffold's job count. Each job runs in its own thread on its own
interval; distributed locks (where a job uses one) keep multiple scheduler
replicas from double-running the same job."""
import time
import threading
from packages.observability.logging import get_logger
from wasteos_scheduler.jobs import hotspot_detection, cleanup, outbox_flush

logger = get_logger("scheduler")

JOBS = [
    (hotspot_detection.run, 300),    # every 5 minutes
    (outbox_flush.run, 30),          # every 30 seconds
    (cleanup.run, 86400),            # once a day
]


def _run_loop(job_fn, interval_seconds: int):
    while True:
        try:
            job_fn()
        except Exception as e:
            logger.error(f"Scheduled job {job_fn.__module__} failed: {e}")
        time.sleep(interval_seconds)


def main():
    logger.info(f"Starting scheduler with {len(JOBS)} jobs")
    threads = [threading.Thread(target=_run_loop, args=(fn, interval), daemon=True) for fn, interval in JOBS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
