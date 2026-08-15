import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
import plotly.express as px


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Student Career Analytics",
    page_icon="🎓",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    opacity: 0.75;
    margin-bottom: 25px;
}

.section-card {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.25);
    background-color: rgba(128,128,128,0.06);
    margin-bottom: 20px;
}

.ai-card {
    padding: 24px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.25);
    background-color: rgba(128,128,128,0.08);
    margin-top: 10px;
    margin-bottom: 20px;
}

.ai-title {
    font-size: 24px;
    font-weight: 750;
}

.ai-description {
    font-size: 15px;
    opacity: 0.8;
    margin-top: 6px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# TITLE
# ==================================================

st.markdown(
    '<div class="main-title">🎓 AI Student Career Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Student Performance & Career Recommendation Dashboard'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# LOAD DATASET
# ==================================================

df = pd.read_csv(
    r"D:\AI_Student_Career_Analytics\data\student_data.csv"
)


# ==================================================
# SUBJECTS
# ==================================================

subjects = [
    "Python",
    "SQL",
    "ML",
    "Communication",
    "Math"
]


# ==================================================
# CALCULATE OVERALL SCORE
# ==================================================

df["Overall_Score"] = df[subjects].mean(axis=1)


# ==================================================
# STUDENT SELECTION
# ==================================================

st.subheader("👨‍🎓 Select Student")

student_name = st.selectbox(
    "Choose a student",
    df["Student"].tolist()
)

student = df[
    df["Student"] == student_name
].iloc[0]


st.divider()


# ==================================================
# STUDENT OVERVIEW
# ==================================================

st.subheader("📌 Student Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Overall Score",
        f"{student['Overall_Score']:.2f}"
    )

with col2:
    st.metric(
        "Projects Completed",
        int(student["Projects"])
    )

with col3:
    st.metric(
        "Placement Status",
        str(student["Placement"])
    )


# ==================================================
# SKILL ANALYSIS
# ==================================================

st.subheader("📊 Skill Analysis")

skill_data = pd.DataFrame({
    "Skill": subjects,
    "Score": [
        student[skill]
        for skill in subjects
    ]
})


fig = px.bar(
    skill_data,
    x="Skill",
    y="Score",
    text="Score",
    range_y=[0, 100]
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Skills",
    yaxis_title="Score",
    xaxis=dict(
        tickangle=0
    ),
    height=430,
    margin=dict(
        l=20,
        r=20,
        t=30,
        b=60
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==================================================
# STRONG & WEAK SKILLS
# ==================================================

strong_skills = [
    skill
    for skill in subjects
    if student[skill] >= 70
]

weak_skills = [
    skill
    for skill in subjects
    if student[skill] < 70
]


col1, col2 = st.columns(2)


with col1:

    st.subheader("💪 Strong Skills")

    if strong_skills:

        for skill in strong_skills:
            st.success(skill)

    else:

        st.info(
            "No strong skills above 70."
        )


with col2:

    st.subheader("⚠️ Skill Gaps")

    if weak_skills:

        for skill in weak_skills:
            st.warning(skill)

    else:

        st.success(
            "No major skill gaps."
        )


# ==================================================
# PROJECTS
# ==================================================

st.subheader("📁 Projects Completed")

st.info(
    f"Student has completed {int(student['Projects'])} project(s)."
)


st.divider()


# ==================================================
# PLACEMENT PREDICTION
# ==================================================

st.subheader("🎯 Placement Prediction")

features = [
    "Python",
    "SQL",
    "ML",
    "Communication",
    "Math",
    "Projects"
]

X_student = pd.DataFrame(
    [[student[feature] for feature in features]],
    columns=features
)


# Default values
placement_probability = None
prediction = None


try:

    import joblib

    model = joblib.load(
        r"D:\AI_Student_Career_Analytics\models\placement_model.pkl"
    )

    prediction = model.predict(
        X_student
    )[0]


    # ------------------------------------------------
    # ACTUAL MODEL PROBABILITY
    # ------------------------------------------------

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            X_student
        )[0]

        placement_probability = probabilities[1] * 100


    # ------------------------------------------------
    # DISPLAY PREDICTION
    # ------------------------------------------------

    if prediction == 1:

        st.success(
            "🎉 Placement Prediction: Likely to be PLACED"
        )

    else:

        st.warning(
            "⚠️ Placement Prediction: Needs Improvement"
        )


    # ------------------------------------------------
    # DISPLAY PROBABILITY
    # ------------------------------------------------

    if placement_probability is not None:

        st.metric(
            "📈 Placement Probability",
            f"{placement_probability:.1f}%"
        )

        st.progress(
            int(round(placement_probability))
        )

        st.caption(
            "Model Placement Probability — not a guaranteed real-world placement outcome."
        )

    else:

        st.info(
            "The current model does not provide probability scores."
        )


except FileNotFoundError:

    st.error(
        "Placement model not found. Please train the model first."
    )


# ==================================================
# PERFORMANCE SUMMARY
# ==================================================

st.divider()

st.subheader("📈 Performance Summary")


# Find strongest and lowest skills

strongest_skill = max(
    subjects,
    key=lambda skill: student[skill]
)

lowest_skill = min(
    subjects,
    key=lambda skill: student[skill]
)


summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)


with summary_col1:

    st.metric(
        "Overall Score",
        f"{student['Overall_Score']:.2f}"
    )


with summary_col2:

    st.metric(
        "🏆 Strongest Skill",
        f"{strongest_skill} ({student[strongest_skill]:.0f})"
    )


with summary_col3:

    st.metric(
        "📌 Lowest Skill",
        f"{lowest_skill} ({student[lowest_skill]:.0f})"
    )


with summary_col4:

    if placement_probability is not None:

        st.metric(
            "🎯 Placement Probability",
            f"{placement_probability:.1f}%"
        )

    else:

        st.metric(
            "🎯 Placement Probability",
            "N/A"
        )


# ==================================================
# AI CAREER RECOMMENDATION
# ==================================================

st.divider()

st.subheader("🤖 AI Career Recommendation")


st.markdown("""
<div class="ai-card">

<div class="ai-title">
🤖 Personalized AI Career Advisor
</div>

<div class="ai-description">
Get an AI-powered career recommendation based on the student's
skills, academic performance, projects and placement prediction.
</div>

</div>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================

if "ai_recommendation" not in st.session_state:

    st.session_state.ai_recommendation = None

if "ai_student" not in st.session_state:

    st.session_state.ai_student = None


# ==================================================
# AI BUTTON
# ==================================================

if st.button(
    "🚀 Generate AI Recommendation",
    use_container_width=True
):

    load_dotenv()

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )


    # ------------------------------------------------
    # CHECK API KEY
    # ------------------------------------------------

    if not api_key:

        st.error(
            "GEMINI_API_KEY not found in .env file."
        )


    else:

        client = genai.Client(
            api_key=api_key
        )


        # ------------------------------------------------
        # AI PROMPT
        # ------------------------------------------------

        prompt = f"""
You are a career advisor for engineering students.

Student: {student["Student"]}

Python Score: {student["Python"]}
SQL Score: {student["SQL"]}
Machine Learning Score: {student["ML"]}
Communication Score: {student["Communication"]}
Math Score: {student["Math"]}

Projects Completed: {student["Projects"]}

Overall Score: {student["Overall_Score"]:.2f}

Strong Skills: {strong_skills}

Skill Gaps: {weak_skills}


Provide the answer in exactly these sections:

1. BEST CAREER ROLES

Give the best 2 career roles for this student.


2. WHY THESE ROLES MATCH

Explain why each role matches the student's skills.


3. SKILLS TO IMPROVE

Give exactly 3 skills the student should improve.


4. LEARNING ROADMAP

Give a practical 3-month learning roadmap.


Keep the response concise, professional and practical.
"""


        # ------------------------------------------------
        # GEMINI REQUEST
        # ------------------------------------------------

        try:

            with st.spinner(
                "🤖 AI is analyzing the student's profile..."
            ):

                interaction = client.interactions.create(
                    model="gemini-3.5-flash",
                    input=prompt
                )


            # Save recommendation
            st.session_state.ai_recommendation = (
                interaction.output_text
            )

            st.session_state.ai_student = (
                student["Student"]
            )

            st.success(
                "✅ AI Recommendation Generated Successfully"
            )


        except Exception as e:

            st.error(
                f"AI request failed: {e}"
            )


# ==================================================
# DISPLAY SAVED AI RECOMMENDATION
# ==================================================

if (
    st.session_state.ai_recommendation
    and
    st.session_state.ai_student == student["Student"]
):

    st.markdown(
        "### 💡 Career Recommendation"
    )

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.write(
        st.session_state.ai_recommendation
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "🎓 AI Student Career Analytics | "
    "Student Performance • Placement Prediction • "
    "AI Career Recommendation"
)