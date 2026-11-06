🎓 Student Performance Predictor

An interactive Machine Learning web application built with Streamlit and Scikit-Learn to predict student academic outcomes (Pass/Fail) based on study habits, attendance, tutoring, and parental support metrics.

📌 Project Overview

This application helps educators and administrators identify students who might need academic intervention early on. By analyzing key indicators such as weekly study hours, attendance ratio, external tutoring, and parental support levels, the underlying Machine Learning model predicts the likelihood of a student passing or failing.

Originally built with a Flask backend and vanilla HTML/JS frontend, the project has been fully migrated to Streamlit for a faster, single-file pure Python UI/UX and native session management.

✨ Features

🔮 ML Performance Prediction: Input student details to get real-time predictions powered by a trained Machine Learning model.

📊 Interactive UI: User-friendly input forms with dynamic inputs and automatic feature engineering (e.g., calculating attendance ratios).

🔐 Admin Panel: Secure, password-protected administrative interface (st.session_state based authentication).

📈 Data Records: View historical prediction logs and export submission data directly to a downloadable CSV file.

🛠️ Tech Stack & Dependencies

Language: Python 3.10+

Frontend & App Framework: Streamlit

Machine Learning: Scikit-Learn, Joblib

Data Manipulation: Pandas

📁 Project Structure

Student_Performance_Prediction/
├── app.py                  # Main Streamlit application entrypoint
├── model.pkl               # Trained ML pipeline model
├── student_data.csv        # Database of submitted student records (auto-generated)
├── requirements.txt        # Python package dependencies
├── .gitignore              # Files/directories ignored by Git
└── README.md               # Project documentation


🚀 Getting Started

Follow these steps to run the application locally on your machine.

1. Prerequisites

Ensure you have Python 3.10+ installed.

2. Set Up Virtual Environment

Clone the repository and set up a virtual environment:

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate
# Linux / macOS:
source .venv/bin/activate


3. Install Dependencies

Install all required libraries using pip:

pip install streamlit pandas scikit-learn joblib


4. Run the Application

Launch the Streamlit app:

streamlit run app.py


Open your browser and navigate to http://localhost:8501.

🔐 Admin Panel Credentials

To log into the Admin Panel within the application interface:

Username: admin

Password: admin123

📝 Machine Learning Pipeline

The model utilizes a Scikit-Learn Pipeline composed of:

OneHotEncoder for categorical features (Gender, Tutoring, ParentalSupport).

Passthrough Transformer for numeric features (StudyTimeWeekly, AttendanceRatio).

Logistic Regression / Random Forest classifier for binary output (1 = Pass, 0 = Fail).

📄 License

This project is open-source and available under the MIT License.