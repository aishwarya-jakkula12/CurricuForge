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

# ---------------- LIGHT + BROWN THEME CSS ----------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #fafaf9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f3ede7;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #3b2f2f;
}

/* Buttons */
.stButton>button {
    background-color: #7c3f00;
    color: white;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #6a3400;
}

/* Week cards */
.week-card {
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 16px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.06);
}

/* Normal learning week */
.normal-week {
    background-color: #ffffff;
    border-left: 6px solid #d6ccc2;
}

/* Project-related week */
.project-week {
    background-color: #ecfdf5;
    border-left: 6px solid #22c55e;
}

/* Headings */
h1 {
    color: #5c2e00;
}
h2, h3, h4 {
    color: #3b2f2f;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>📘 CurricuForge</h1>
    <h4 style='text-align:center;color:#7c3f00;'>
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

generate_btn = st.sidebar.button("🚀 Generate Schedule")

# ---------------- GENERATE PLAN ----------------
if generate_btn:
    curriculum = generate_curriculum(subject, level)
    plan = create_weekly_plan(curriculum, duration)

    st.session_state["plan"] = plan

# ---------------- DISPLAY SCHEDULE ----------------
if "plan" in st.session_state:
    st.subheader("📆 Preparation Schedule")

    cols = st.columns(2)

    for idx, week in enumerate(st.session_state["plan"]):
        col = cols[idx % 2]

        # ✅ FIX: Detect project presence in ANY unit
        is_project_week = any(
            "Project" in unit["topic"]
            for unit in week["units"]
        )

        card_class = "project-week" if is_project_week else "normal-week"

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
                    f"- **{unit['topic']}**  \n<span style='color:#6b4f3f;'>{unit['subtopic']}</span>",
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
            f"Missed Week {missed_week} topics were merged smoothly into upcoming weeks."
        )

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center;color:#7c3f00;'>
    CurricuForge • Clean • Adaptive • Project-Oriented
    </p>
    """,
    unsafe_allow_html=True
)
