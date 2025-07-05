import time
import datetime

def scheduler_loop():
    print("Scheduler Started...")

    while True:
        now = datetime.datetime.now()
        next_minute = (now.replace(second=0, microsecond=0) + datetime.timedelta(minutes=1))
        print(now)
        sleep_time = (next_minute - datetime.datetime.now()).total_seconds()
        print(f"sleeping {sleep_time}")
        time.sleep(max(sleep_time,0))

scheduler_loop()