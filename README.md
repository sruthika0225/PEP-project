# 🔔 Task Alarm & Reminder

A Flask-based task reminder application with scheduled alarms, snooze, dismiss, repeating reminders and SQLite storage.

## Features

- Create, edit and delete reminders
- Schedule an alarm using date and time
- Once, daily and weekday repeating reminders
- Alarm screen with sound
- Snooze for 5 minutes
- Dismiss alarms
- Complete tasks
- SQLite database
- Automated tests

## Run locally

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open:

`http://127.0.0.1:5000`

## Important

The first version uses browser-side alarm behavior. The web page must remain open for the browser to play the alarm sound reliably.
