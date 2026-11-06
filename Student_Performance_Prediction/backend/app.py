import os
import joblib
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered",
)

# 2. Load ML Model
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# 3. Setup CSV Database File
CSV_FILE = "student_data.csv"
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=[
        "RollNumber", "Gender", "StudyTimeWeekly", "AttendanceRatio",
        "Tutoring", "ParentalSupport", "Prediction"
    ])
    df_init.to_csv(CSV_FILE, index=False)

# 4. Initialize Session State for Admin Authentication
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# 5. Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Student Predictor", "Admin Panel"])

# ==========================================
# PAGE 1: STUDENT PREDICTOR
# ==========================================
if page == "Student Predictor":
    st.title("🎓 Student Performance Predictor")
    st.write("Predict academic outcome using machine learning.")

    with st.form("prediction_form"):
        roll_number = st.text_input("Roll Number", placeholder="Enter roll number")
        
        # UI selections mapped to model-expected numbers from training data
        gender_label = st.selectbox("Gender", ["Select", "Male", "Female"])
        study_time = st.number_input("Study Time (hrs/week)", min_value=0.0, step=0.1, value=15.0)
        total_classes = st.number_input("Total Classes", min_value=1, step=1, value=100)
        classes_attended = st.number_input("Classes Attended", min_value=0, step=1, value=80)
        
        tutoring_label = st.selectbox("Tutoring", ["Select", "Yes", "No"])
        parental_support_label = st.selectbox("Parental Support", ["Select", "Low", "Medium", "High"])

        submit_btn = st.form_submit_button("Predict Result")

    if submit_btn:
        # Validation checks
        if (roll_number == "" or gender_label == "Select" or 
            tutoring_label == "Select" or parental_support_label == "Select"):
            st.error("⚠️ Please fill out all required fields correctly.")
        elif classes_attended > total_classes:
            st.error("⚠️ Classes attended cannot be greater than total classes.")
        else:
            attendance_ratio = classes_attended / total_classes

            # Map user inputs to exact numeric values used during training (source: 12)
            gender_val = 1 if gender_label == "Male" else 0
            tutoring_val = 1 if tutoring_label == "Yes" else 0
            
            # Mapping Parental Support labels to dataset integer codes
            support_mapping = {"Low": 1, "Medium": 2, "High": 3}
            parental_support_val = support_mapping.get(parental_support_label, 1)

            # Prepare dataframe matching the exact feature names and types from training
            input_df = pd.DataFrame([{
                "Gender": gender_val,
                "StudyTimeWeekly": float(study_time),
                "AttendanceRatio": attendance_ratio,
                "Tutoring": tutoring_val,
                "ParentalSupport": parental_support_val
            }])

            # try:
            #     # ML Prediction
            #     prediction = int(model.predict(input_df)[0])

            #     # Save record to CSV
            #     save_df = pd.DataFrame([{
            #         "RollNumber": roll_number,
            #         "Gender": gender_label,
            #         "StudyTimeWeekly": float(study_time),
            #         "AttendanceRatio": attendance_ratio,
            #         "Tutoring": tutoring_label,
            #         "ParentalSupport": parental_support_label,
            #         "Prediction": prediction
            #     }])
            #     save_df.to_csv(CSV_FILE, mode="a", header=False, index=False)

            #     # Display Result
            #     st.markdown("---")
            #     if prediction == 1:
            #         st.success(f"✅ **Student is likely to PASS** (Attendance Ratio: {round(attendance_ratio, 2)})")
            #     else:
            #         st.error(f"❌ **Student is likely to FAIL** (Attendance Ratio: {round(attendance_ratio, 2)})")

            # except Exception as e:
            #     st.error(f"⚠️ Error during prediction: {e}")
            try:
                # 🔍 DEBUG: Print input data to terminal to check values
                print("Input DataFrame Sent to Model:\n", input_df)

                # ML Prediction & Probabilities
                prediction = int(model.predict(input_df)[0])
                probabilities = model.predict_proba(input_df)
                
                print("Model Prediction:", prediction)
                print("Probabilities [Fail, Pass]:", probabilities)

                # Save record to CSV
                save_df = pd.DataFrame([{
                    "RollNumber": roll_number,
                    "Gender": gender_label,
                    "StudyTimeWeekly": float(study_time),
                    "AttendanceRatio": attendance_ratio,
                    "Tutoring": tutoring_label,
                    "ParentalSupport": parental_support_label,
                    "Prediction": prediction
                }])
                save_df.to_csv(CSV_FILE, mode="a", header=False, index=False)

                # Display Result & Probability
                st.markdown("---")
                pass_prob = probabilities[0][1] * 100 # percentage chance of passing
                
                if prediction == 1:
                    st.success(f"✅ **Student is likely to PASS** (Confidence: {pass_prob:.1f}%, Attendance Ratio: {round(attendance_ratio, 2)})")
                else:
                    st.error(f"❌ **Student is likely to FAIL** (Confidence: {100 - pass_prob:.1f}%, Attendance Ratio: {round(attendance_ratio, 2)})")

            except Exception as e:
                st.error(f"⚠️ Error during prediction: {e}")

# ==========================================
# PAGE 2: ADMIN PANEL
# ==========================================
elif page == "Admin Panel":
    st.title("🔐 Admin Panel")

    if not st.session_state.admin_logged_in:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")

        if login_btn:
            if username == "admin" and password == "admin123":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    else:
        if st.button("🚪 Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        st.markdown("---")
        
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            st.info(f"📊 Total Students Submitted: {len(df)}")

            if not df.empty and "Prediction" in df.columns:
                df["Result"] = df["Prediction"].apply(lambda x: "PASS" if x == 1 else "FAIL")

            st.dataframe(df, use_container_width=True)

            with open(CSV_FILE, "rb") as file:
                st.download_button(
                    label="⬇️ Download CSV",
                    data=file,
                    file_name="student_data.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No submission records found yet.")