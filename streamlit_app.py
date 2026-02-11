import streamlit as st
from curriculum_generator import (
    generate_curriculum,
    create_weekly_plan,
    reschedule_from_missed_week
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CurricuForge",
    page_icon="📘",
    layout="wide"
)

# ---------------- STRONG BROWN + LIGHT THEME CSS ----------------
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #fafaf7;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f2e8dc;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #4a2c1a;
    font-weight: 500;
}

/* Buttons */
.stButton>button {
    background-color: #8b4513 !important;
    color: white !important;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 700;
    border: none;
}

.stButton>button:hover {
    background-color: #6f350d !important;
}

/* Week cards */
.week-card {
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Normal weeks */
.normal-week {
    background-color: #ffffff;
    border-left: 6px solid #d6c2b2;
}

/* Project phase weeks */
.project-week {
    background-color: #ecfdf5;
    border-left: 6px solid #16a34a;
}

/* Headings */
h1 {
    color: #6b2e00;
}
h2, h3, h4 {
    color: #4a2c1a;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>📘 CurricuForge</h1>
    <h4 style='text-align:center;color:#8b4513;'>
    Adaptive Preparation Scheduler with Project-Based Learning
    </h4>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("🧠 Preparation Setup")

subject = st.sidebar.text_input("Course / Subject", "Machine Learning")

level = st.sidebar.selectbox(
    "Target Level",
    ["Beginner", "Intermediate", "Advanced"]
)

duration = st.sidebar.slider(
    "Duration (Weeks)",
    min_value=1,
    max_value=20,
    value=6
)

generate_btn = st.sidebar.button("📅 Generate Curriculum")

# ---------------- GENERATE PLAN ----------------
if generate_btn:
    curriculum = generate_curriculum(subject, level)
    plan = create_weekly_plan(curriculum, duration)

    st.session_state["plan"] = plan

# ---------------- DISPLAY SCHEDULE ----------------
if "plan" in st.session_state:
    st.subheader("📆 Preparation Schedule")

    cols = st.columns(2)

    # ✅ FIX: detect project start week
    project_started = False

    for idx, week in enumerate(st.session_state["plan"]):
        col = cols[idx % 2]

        # If any unit contains Project → mark project phase started
        if any("Project" in u["topic"] for u in week["units"]):
            project_started = True

        # Apply green to ALL weeks after project starts
        card_class = "project-week" if project_started else "normal-week"

        with col:
            st.markdown(
                f"""
                <div class="week-card {card_class}">
                    <h4>Week {week['week']}</h4>
                """,
                unsafe_allow_html=True
            )

            for unit in week["units"]:
                st.markdown(
                    f"- **{unit['topic']}**  \n<span style='color:#5c4033;'>{unit['subtopic']}</span>",
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- RESCHEDULING ----------------
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🔄 Reschedule After Interruption")

    missed_week = st.number_input(
        "Select the week you missed",
        min_value=1,
        max_value=len(st.session_state["plan"]),
        value=1
    )

    if st.button("♻️ Reschedule Preparation"):
        updated_plan = reschedule_from_missed_week(
            st.session_state["plan"],
            missed_week
        )

        st.session_state["plan"] = updated_plan

        st.success(
            f"Missed Week {missed_week} topics were merged into upcoming weeks."
        )

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center;color:#8b4513;'>
    CurricuForge • Professional • Adaptive • Project-Oriented
    </p>
    """,
    unsafe_allow_html=True
)
