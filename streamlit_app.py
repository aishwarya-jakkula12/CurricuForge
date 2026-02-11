import streamlit as st
from curriculum_generator import (
    generate_curriculum,
    create_weekly_plan,
    reschedule_from_missed_week
)

st.set_page_config(page_title="CurricuForge", layout="centered")

st.title("📚 CurricuForge – Adaptive Preparation Scheduler")
st.write("Generate and adapt a realistic preparation schedule")

# ---------------- USER INPUTS ----------------

subject = st.text_input("Enter Subject / Course", "Machine Learning")

level = st.selectbox(
    "Select Level",
    ["Beginner", "Intermediate", "Advanced"]
)

duration = st.number_input(
    "Number of Weeks",
    min_value=1,
    max_value=20,
    value=6
)

st.divider()

# ---------------- GENERATE PLAN ----------------

if st.button("Generate Curriculum"):
    curriculum = generate_curriculum(subject, level)
    weekly_plan = create_weekly_plan(curriculum, duration)

    st.session_state["plan"] = weekly_plan
    st.session_state["subject"] = subject
    st.session_state["level"] = level
    st.session_state["duration"] = duration

# ---------------- DISPLAY PLAN ----------------

if "plan" in st.session_state:
    st.subheader("📆 Preparation Schedule")

    for week in st.session_state["plan"]:
        with st.expander(f"Week {week['week']}"):
            for unit in week["units"]:
                st.markdown(
                    f"- **{unit['topic']}** — {unit['subtopic']}"
                )

    st.divider()

    # ---------------- RESCHEDULING ----------------
    st.subheader("🔄 Missed a Week? Reschedule")

    missed_week = st.number_input(
        "Enter Missed Week Number",
        min_value=1,
        max_value=len(st.session_state["plan"]),
        value=1
    )

    if st.button("Reschedule Preparation"):
        updated_plan = reschedule_from_missed_week(
            st.session_state["plan"],
            missed_week
        )

        st.session_state["plan"] = updated_plan

        st.success(
            f"Schedule updated! Missed Week {missed_week} topics merged."
        )

        st.subheader("📆 Updated Preparation Schedule")

        for week in updated_plan:
            with st.expander(f"Week {week['week']}"):
                for unit in week["units"]:
                    st.markdown(
                        f"- **{unit['topic']}** — {unit['subtopic']}"
                    )
