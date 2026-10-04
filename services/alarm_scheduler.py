from datetime import datetime, timedelta
from threading import Thread, Event
from database import db

class AlarmScheduler:
    def __init__(self):
        self.stop_event = Event()
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return

        self.thread = Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while not self.stop_event.is_set():
            self.check_alarms()
            self.stop_event.wait(10)

    def check_alarms(self):
        now = datetime.now().replace(second=0, microsecond=0)

        for task in db.get_active_tasks():
            try:
                alarm_time = datetime.strptime(
                    f"{task['alarm_date']} {task['alarm_time']}",
                    "%Y-%m-%d %H:%M"
                )
            except ValueError:
                continue

            if alarm_time == now and not task["alarm_triggered"]:
                # The browser polls /api/tasks and handles the actual sound/UI.
                # Marking is intentionally left to the browser's dismiss call.
                pass

            # Daily/weekday alarms are advanced after their scheduled time.
            if alarm_time < now and task["repeat"] in ("daily", "weekdays"):
                should_advance = task["alarm_date"] != now.strftime("%Y-%m-%d")
                if should_advance:
                    next_date = alarm_time + timedelta(days=1)
                    if task["repeat"] == "weekdays":
                        while next_date.weekday() >= 5:
                            next_date += timedelta(days=1)
                    db.update_alarm_time(
                        task["id"],
                        next_date.strftime("%Y-%m-%d"),
                        task["alarm_time"]
                    )

scheduler = AlarmScheduler()
