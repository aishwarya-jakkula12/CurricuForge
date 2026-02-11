import streamlit as st
from curriculum_generator import (
    generate_curriculum,
    create_weekly_plan,
    reschedule_from_missed_week
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CurricuForge – Smart Preparation Planner",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #faf7f2;
}

.sidebar .sidebar-content {
    background-color: #f3e9dc;
}

.block-container {
    padding-top: 2rem;
}

.week-card {
    background-color: #ffffff;
    border-left: 8px solid #8b5e3c;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 10px;
}

.week-card-project {
    background-color: #eefbf3;
    border-left: 8px solid #2e8b57;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 10px;
}

button[kind="primary"] {
    background-color: #8b5e3c;
    color: white;
}

h1, h2, h3 {
    color: #4a2c2a;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 📚 Preparation Setup")

course = st.sidebar.selectbox(
    "Course / Subject",
    [
        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",
        "Web Development",
        "Cyber Security"
    ]
)

level = st.sidebar.selectbox(
    "Target Level",
    ["Beginner", "Intermediate", "Advanced"]
)

duration = st.sidebar.slider(
    "Duration (Weeks)",
    min_value=2,
    max_value=12,
    value=6
)

generate = st.sidebar.button("🚀 Generate Curriculum")

# ---------------- MAIN LOGIC ----------------
if generate:
    curriculum = generate_curriculum(course, level)
    plan = create_weekly_plan(curriculum, duration)

    st.session_state["plan"] = plan
    st.session_state["course"] = course
    st.session_state["level"] = level
    st.session_state["duration"] = duration

# ---------------- DISPLAY CURRICULUM ----------------
if "plan" in st.session_state:
    st.markdown("## 🎯 Generated Curriculum")
    st.write(f"**Course:** {st.session_state['course']}")
    st.write(f"**Level:** {st.session_state['level']}")
    st.write(f"**Duration:** {st.session_state['duration']} weeks")
    st.markdown("---")

    for week in st.session_state["plan"]:
        is_project = any("Project" in u["topic"] for u in week["units"])

        card_class = "week-card-project" if is_project else "week-card"

        st.markdown(
            f"<div class='{card_class}'>"
            f"<h3>Week {week['week']}</h3>",
            unsafe_allow_html=True
        )

        for unit in week["units"]:
            st.markdown(
                f"• **{unit['topic']}** — {unit['subtopic']}"
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- RESCHEDULING ----------------
    st.markdown("## 🔄 Missed a Week?")
    missed_week = st.number_input(
        "Enter missed week number",
        min_value=1,
        max_value=len(st.session_state["plan"]),
        step=1
    )

    if st.button("Reschedule"):
        new_plan = reschedule_from_missed_week(
            st.session_state["plan"],
            missed_week
        )

        st.markdown("## ✅ Rescheduled Curriculum")
        for week in new_plan:
            is_project = any("Project" in u["topic"] for u in week["units"])
            card_class = "week-card-project" if is_project else "week-card"

            st.markdown(
                f"<div class='{card_class}'>"
                f"<h3>Week {week['week']}</h3>",
                unsafe_allow_html=True
            )

            for unit in week["units"]:
                st.markdown(
                    f"• **{unit['topic']}** — {unit['subtopic']}"
                )

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("🔁 **Tip:** Missed topics are automatically merged into upcoming weeks without breaking learning continuity.")
