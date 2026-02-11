# =====================================================
# Final Preparation-Oriented Curriculum Generator
# =====================================================


def generate_curriculum(subject, level):
    """
    Defines curriculum topics with subtopics,
    including a proper project phase.
    """

    curriculum = [
        {
            "topic": f"Introduction to {subject}",
            "subtopics": [
                "What is " + subject,
                "Applications",
                "Learning Workflow",
                "Tools & Environment Setup"
            ]
        },
        {
            "topic": "Fundamental Concepts",
            "subtopics": [
                "Data and Features",
                "Labels and Targets",
                "Train-Test Split",
                "Evaluation Basics"
            ]
        },
        {
            "topic": "Core Concepts",
            "subtopics": [
                "Supervised Learning",
                "Unsupervised Learning",
                "Model Training",
                "Overfitting & Underfitting"
            ]
        },
        {
            "topic": "Advanced Techniques",
            "subtopics": [
                "Ensemble Methods",
                "Hyperparameter Tuning",
                "Model Optimization"
            ]
        },
        {
            "topic": "Project (Hands-on)",
            "subtopics": [
                "Problem Definition & Dataset Selection",
                "Data Preprocessing",
                "Model Building",
                "Model Evaluation",
                "Result Analysis & Presentation"
            ]
        }
    ]

    if level == "Beginner":
        return curriculum[:3] + [curriculum[-1]]
    elif level == "Intermediate":
        return curriculum[:4] + [curriculum[-1]]
    else:
        return curriculum


def create_weekly_plan(curriculum, duration):
    """
    Distributes topic subtopics week-wise
    to create a proper preparation schedule.
    """

    units = []

    # Flatten topic + subtopic pairs
    for block in curriculum:
        for sub in block["subtopics"]:
            units.append({
                "topic": block["topic"],
                "subtopic": sub
            })

    total_units = len(units)
    plan = []

    for week in range(1, duration + 1):
        start = (week - 1) * total_units // duration
        end = week * total_units // duration

        plan.append({
            "week": week,
            "units": units[start:end]
        })

    return plan


def reschedule_from_missed_week(plan, missed_week):
    """
    Visibly reschedules by merging missed week's units
    into the immediate next week.
    """

    if missed_week < 1 or missed_week >= len(plan):
        return plan

    new_plan = []

    for i, week in enumerate(plan):
        # Skip the missed week
        if i == missed_week - 1:
            continue

        # If this is the week immediately after the missed week
        if i == missed_week:
            merged_units = plan[missed_week - 1]["units"] + week["units"]
            new_plan.append({
                "week": len(new_plan) + 1,
                "units": merged_units
            })
        else:
            new_plan.append({
                "week": len(new_plan) + 1,
                "units": week["units"]
            })

    return new_plan
