def get_alarm_message(task):
    return {
        "title": "Alarm",
        "task": task["title"],
        "description": task.get("description", "")
    }
