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

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>📘 CurricuForge</h1>
    <h4 style='text-align:center;color:gray;'>
    Adaptive Preparation Scheduler with Project-Based Learning
    </h4>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("🧠 Preparation Details")

subject = st.sidebar.text_input(
    "Course / Subject",
    "Machine Learning"
)

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
    st.session_state["subject"] = subject
    st.session_state["level"] = level
    st.session_state["duration"] = duration

# ---------------- DISPLAY SCHEDULE ----------------
if "plan" in st.session_state:
    st.subheader("📆 Preparation Schedule")

    cols = st.columns(2)

    for idx, week in enumerate(st.session_state["plan"]):
        col = cols[idx % 2]

        with col:
            is_project = any("Project" in u["topic"] for u in week["units"])

            box_color = "#E8F8F5" if is_project else "#F4F6F7"

            st.markdown(
                f"""
                <div style="
                    background-color:{box_color};
                    padding:15px;
                    border-radius:10px;
                    margin-bottom:15px;
                    box-shadow:0px 2px 6px rgba(0,0,0,0.1);
                ">
                <h4>Week {week['week']}</h4>
                """,
                unsafe_allow_html=True
            )

            for unit in week["units"]:
                st.markdown(
                    f"- **{unit['topic']}**  \n  <span style='color:gray;'>{unit['subtopic']}</span>",
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
            f"Preparation rescheduled successfully! Missed Week {missed_week} topics were merged into upcoming weeks."
        )

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center;color:gray;'>
    CurricuForge • Built for realistic and adaptive learning
    </p>
    """,
    unsafe_allow_html=True
)
