import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from dotenv import load_dotenv
from google import genai


df = pd.read_csv(r"D:\AI_Student_Career_Analytics\data\student_data.csv")
print("STUDENT DATASET")
print(df)
subjects = ["Python", "SQL", "ML", "Communication", "Math"]
print("\nAVERAGE SCORES")
print(df[subjects].mean())

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

averages = df[subjects].mean()

plt.figure(figsize=(8, 5))
plt.bar(subjects, averages)

plt.title("Average Student Skill Scores")
plt.xlabel("Skills")
plt.ylabel("Average Score")

plt.show()
# Calculate overall score
df["Overall_Score"] = df[subjects].mean(axis=1)

print("\nOVERALL STUDENT SCORES")
print(df[["Student", "Overall_Score"]])

# Student performance chart
plt.figure(figsize=(10, 5))
plt.bar(df["Student"], df["Overall_Score"])

plt.title("Overall Student Performance")
plt.xlabel("Students")
plt.ylabel("Overall Score")
plt.xticks(rotation=45)

plt.show()
print("\nSKILL GAP ANALYSIS")

for index, row in df.iterrows():
    weak_skills = []

    for subject in subjects:
        if row[subject] < 70:
            weak_skills.append(subject)

    print(row["Student"], "->", weak_skills)

# Features and target
features = ["Python", "SQL", "ML", "Communication", "Math", "Projects"]

X = df[features]
y = df["Placement"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Create and train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)

print("\nPLACEMENT PREDICTION MODEL")
print("Accuracy:", accuracy)

print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, y_pred))
joblib.dump(model, "models/placement_model.pkl")

print("\nML MODEL SAVED SUCCESSFULLY")
print("\nCAREER PROFILE")

for index, row in df.iterrows():
    weak_skills = []

    for subject in subjects:
        if row[subject] < 70:
            weak_skills.append(subject)

    print("\nStudent:", row["Student"])
    print("Overall Score:", round(row["Overall_Score"], 2))
    print("Strong Skills:", [
        subject for subject in subjects if row[subject] >= 70
    ])
    print("Skill Gaps:", weak_skills)
    print("Projects:", row["Projects"])
    load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("\nPERSONALIZED AI CAREER RECOMMENDATIONS")

for index, row in df.iterrows():

    strong_skills = [
        subject for subject in subjects
        if row[subject] >= 70
    ]

    weak_skills = [
        subject for subject in subjects
        if row[subject] < 70
    ]

    prompt = f"""
You are a career advisor for engineering students.

Student: {row["Student"]}
Python Score: {row["Python"]}
SQL Score: {row["SQL"]}
Machine Learning Score: {row["ML"]}
Communication Score: {row["Communication"]}
Math Score: {row["Math"]}
Projects Completed: {row["Projects"]}
Overall Score: {row["Overall_Score"]:.2f}

Strong Skills: {strong_skills}
Skill Gaps: {weak_skills}

Provide:
1. Best 2 career roles for this student.
2. Why these roles match the student.
3. Three skills the student should improve.
4. A short learning roadmap.
"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=prompt
    )

    print(f"\n--- {row['Student']} ---")
    print(interaction.output_text)

    print("\nAI INTERVIEW QUESTION GENERATOR")

# Use the first student as an example
student = df.iloc[0]

strong_skills = [
    subject for subject in subjects
    if student[subject] >= 70
]

weak_skills = [
    subject for subject in subjects
    if student[subject] < 70
]

interview_prompt = f"""
You are an interview preparation assistant.

Student: {student["Student"]}
Strong Skills: {strong_skills}
Skill Gaps: {weak_skills}
Projects Completed: {student["Projects"]}

Generate 5 technical interview questions for this student.

Requirements:
- 2 Python questions
- 1 SQL question
- 1 Machine Learning question
- 1 project-based question

Give a short expected answer point for each question.
"""

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=interview_prompt
)

print(f"\nInterview Questions for {student['Student']}:")
print(interaction.output_text)