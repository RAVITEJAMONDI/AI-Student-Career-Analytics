# 🎓 AI Student Career Analytics

AI-powered dashboard for analyzing student performance, predicting placement probability, identifying skill strengths and gaps, and generating personalized AI career recommendations.

## 🚀 Features

- 👨‍🎓 Student performance analysis
- 📊 Interactive skill score visualization
- 💪 Strong skill identification
- ⚠️ Skill gap identification
- 📁 Project completion tracking
- 🎯 Machine Learning placement prediction
- 📈 Placement probability
- 🤖 AI-powered career recommendations
- 🗺️ Personalized learning roadmap
- 🎨 Interactive Streamlit dashboard

## 🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn
- Joblib
- Streamlit
- Plotly
- Google GenAI
- python-dotenv

## 📂 Project Structure

```text
AI_Student_Career_Analytics/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── student_data.csv
│
├── models/
│   └── placement_model.pkl
│
└── src/
    └── data_analysis.py
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/RAVITEJAMONDI/AI-Student-Career-Analytics.git
cd AI-Student-Career-Analytics
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

### 4. Install the required dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root directory and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ Never upload your actual API key or `.env` file to GitHub.

## ▶️ How to Run

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your default web browser.

## 🧠 Project Workflow

```text
Student Data
     ↓
Performance Analysis
     ↓
Skill Strengths & Skill Gaps
     ↓
Machine Learning Model
     ↓
Placement Probability
     ↓
AI Career Recommendations
     ↓
Personalized Learning Roadmap
```

## 📊 Expected Output

The dashboard provides:

- 📈 Student performance insights
- 💪 Skill strengths identification
- ⚠️ Skill gap analysis
- 📁 Project completion tracking
- 🎯 Placement probability prediction
- 🤖 AI-powered career recommendations
- 🗺️ Personalized learning roadmap

## 🔐 Security

- API keys are stored using environment variables.
- Sensitive credentials should not be committed to the repository.
- The `.env` file should remain local and should be included in `.gitignore`.

## 📌 Future Enhancements

- 📊 Advanced student performance analytics
- 👥 Multi-student comparison
- 📄 Automated resume analysis
- 🎯 Job-role matching
- 📚 Course recommendation system
- ☁️ Cloud deployment
- 📱 Responsive dashboard improvements

## 👨‍💻 Author

**Ravi Teja Mondi**

B.Tech Student | AI & Full-Stack Enthusiast

---

⭐ If you find this project useful, consider giving it a star on GitHub!