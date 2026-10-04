from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from datetime import datetime
from database.db import init_db
from database import db
from services.alarm_scheduler import scheduler

app = Flask(__name__)
app.config.from_object("config.Config")

init_db()
scheduler.start()

@app.route("/")
def index():
    tasks = db.get_tasks()
    stats = db.get_stats()
    return render_template("index.html", tasks=tasks, stats=stats)

@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        alarm_date = request.form.get("alarm_date", "")
        alarm_time = request.form.get("alarm_time", "")
        repeat = request.form.get("repeat", "once")

        if not title or not alarm_date or not alarm_time:
            return render_template(
                "add_task.html",
                error="Title, date and time are required."
            )

        db.create_task(title, description, alarm_date, alarm_time, repeat)
        return redirect(url_for("index"))

    return render_template("add_task.html")

@app.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = db.get_task(task_id)
    if task is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        alarm_date = request.form.get("alarm_date", "")
        alarm_time = request.form.get("alarm_time", "")
        repeat = request.form.get("repeat", "once")

        if not title or not alarm_date or not alarm_time:
            return render_template(
                "edit_task.html",
                task=task,
                error="Title, date and time are required."
            )

        db.update_task(
            task_id, title, description, alarm_date, alarm_time, repeat
        )
        return redirect(url_for("index"))

    return render_template("edit_task.html", task=task)

@app.post("/delete-task/<int:task_id>")
def delete_task(task_id):
    db.delete_task(task_id)
    return redirect(url_for("index"))

@app.post("/complete-task/<int:task_id>")
def complete_task(task_id):
    db.complete_task(task_id)
    return redirect(url_for("index"))

@app.post("/snooze-task/<int:task_id>")
def snooze_task(task_id):
    task = db.get_task(task_id)
    if task is None:
        abort(404)

    from datetime import timedelta
    new_time = datetime.now() + timedelta(minutes=5)
    db.update_alarm_time(
        task_id,
        new_time.strftime("%Y-%m-%d"),
        new_time.strftime("%H:%M")
    )
    return jsonify({"success": True, "message": "Alarm snoozed for 5 minutes."})

@app.get("/api/tasks")
def api_tasks():
    return jsonify(db.get_active_tasks())

@app.post("/api/alarm/<int:task_id>/dismiss")
def dismiss_alarm(task_id):
    db.mark_alarm_triggered(task_id)
    return jsonify({"success": True})

@app.route("/reuse-task/<int:task_id>")
def reuse_task(task_id):
    task = db.get_task(task_id)

    if task is None:
        abort(404)

    db.reuse_task(task_id)

    return redirect(url_for("edit_task", task_id=task_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
