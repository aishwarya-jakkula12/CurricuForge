import streamlit as st
from curriculum_generator import (
    generate_curriculum,
    create_weekly_plan,
    reschedule_from_missed_week
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CurricuForge – CSE Preparation Planner",
    page_icon="🎓",
    layout="wide"
)

# ---------------- LIGHT + BROWN THEME ----------------
st.markdown("""
<style>
.stApp {
    background-color: #faf7f2;
}

section[data-testid="stSidebar"] {
    background-color: #f3e9dc;
}

section[data-testid="stSidebar"] * {
    color: #4a2c2a;
    font-weight: 500;
}

.stButton>button {
    background-color: #8b5e3c !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 700;
}

.stButton>button:hover {
    background-color: #6f3f24 !important;
}

.week-card {
    background-color: #ffffff;
    border-left: 8px solid #c4a484;
    padding: 16px;
    margin-bottom: 16px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
}

.week-card-project {
    background-color: #ecfdf5;
    border-left: 8px solid #2e8b57;
    padding: 16px;
    margin-bottom: 16px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
}

h1 {
    color: #5c2e00;
}
h2, h3 {
    color: #4a2c2a;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>🎓 CurricuForge</h1>
    <h4 style='text-align:center;color:#8b5e3c;'>
    Adaptive Preparation Scheduler for Computer Science Engineering
    </h4>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.markdown("## 📚 CSE Preparation Setup")

course = st.sidebar.selectbox(
    "Select CSE Course",
    [
        "Programming Fundamentals",
        "Data Structures & Algorithms",
        "Database Management Systems",
        "Operating Systems",
        "Computer Networks",
        "Software Engineering",
        "Web Development",
        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",
        "Cyber Security",
        "Cloud Computing",
        "DevOps"
    ]
)

level = st.sidebar.selectbox(
    "Target Level",
    ["Beginner", "Intermediate", "Advanced"]
)

duration = st.sidebar.slider(
    "Preparation Duration (Weeks)",
    min_value=2,
    max_value=16,
    value=6
)

generate_btn = st.sidebar.button("🚀 Generate Curriculum")

# ---------------- GENERATE PLAN ----------------
if generate_btn:
    curriculum = generate_curriculum(course, level)
    plan = create_weekly_plan(curriculum, duration)

    st.session_state["plan"] = plan
    st.session_state["course"] = course
    st.session_state["level"] = level
    st.session_state["duration"] = duration

# ---------------- DISPLAY CURRICULUM ----------------
if "plan" in st.session_state:
    st.markdown("## 📆 Preparation Schedule")
    st.write(f"**Course:** {st.session_state['course']}")
    st.write(f"**Level:** {st.session_state['level']}")
    st.write(f"**Duration:** {st.session_state['duration']} weeks")
    st.markdown("---")

    project_started = False

    for week in st.session_state["plan"]:
        # Once project starts → keep green for all following weeks
        if any("Project" in u["topic"] for u in week["units"]):
            project_started = True

        card_class = "week-card-project" if project_started else "week-card"

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
    st.markdown("## 🔄 Reschedule After Interruption")

    missed_week = st.number_input(
        "Enter missed week number",
        min_value=1,
        max_value=len(st.session_state["plan"]),
        step=1
    )

    if st.button("♻️ Reschedule Preparation"):
        updated_plan = reschedule_from_missed_week(
            st.session_state["plan"],
            missed_week
        )

        st.session_state["plan"] = updated_plan

        st.success(
            f"Missed Week {missed_week} topics were merged into upcoming weeks successfully."
        )

    st.markdown(
        "<p style='color:#8b5e3c;'>💡 Tip: Project weeks are highlighted in green for clarity.</p>",
        unsafe_allow_html=True
    )

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center;color:#8b5e3c;'>
    CurricuForge • CSE-focused • Adaptive • Project-driven
    </p>
    """,
    unsafe_allow_html=True
)
