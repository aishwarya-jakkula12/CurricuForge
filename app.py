from flask import Flask, render_template, request
from curriculum_generator import (
    generate_curriculum,
    create_weekly_plan,
    reschedule_from_missed_week
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    subject = request.form["subject"]
    level = request.form["level"]
    duration = int(request.form["duration"])

    curriculum = generate_curriculum(subject, level)
    weekly_plan = create_weekly_plan(curriculum, duration)

    return render_template(
        "result.html",
        subject=subject,
        level=level,
        duration=duration,
        plan=weekly_plan
    )


@app.route("/reschedule", methods=["POST"])
def reschedule():
    subject = request.form["subject"]
    level = request.form["level"]
    duration = int(request.form["duration"])
    missed_week = int(request.form["missed_week"])

    curriculum = generate_curriculum(subject, level)
    weekly_plan = create_weekly_plan(curriculum, duration)

    updated_plan = reschedule_from_missed_week(weekly_plan, missed_week)

    return render_template(
        "rescheduled.html",
        subject=subject,
        level=level,
        duration=len(updated_plan),
        plan=updated_plan,
        missed_week=missed_week
    )


if __name__ == "__main__":
    app.run(debug=True)
