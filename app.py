import pickle
import streamlit as st

# Load models separately
with open('random_forest.pkl', 'rb') as f:
    random_forest = pickle.load(f)

with open('svm.pkl', 'rb') as f:
    svm = pickle.load(f)

with open('logistic_regression.pkl', 'rb') as f:
    logistic_regression = pickle.load(f)

# Model dictionary for selection
models = {
    "🌲 Random Forest": random_forest,
    "📈 Logistic Regression": logistic_regression,
    "⚡ SVM": svm
}

# Define prediction function
def prediction(model, Gender, Married, ApplicantIncome, LoanAmount, Credit_History):  
    # Pre-processing user input    
    Gender = 0 if Gender == "Male" else 1
    Married = 0 if Married == "Unmarried" else 1
    Credit_History = 0 if Credit_History == "Unclear Debts" else 1

    LoanAmount = LoanAmount / 1000  # Normalization

    # Making predictions using the selected model
    prediction = model.predict([[Gender, Married, ApplicantIncome, LoanAmount, Credit_History]])

    return 'Approved' if prediction == 1 else 'Rejected'

# Main Streamlit app function
def main():       
    # Front-end UI
    html_temp = """
    <div style="background-color:yellow;padding:13px">
    <h1 style="color:black;text-align:center;">Streamlit Loan Prediction ML App</h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # Model selection using radio buttons with icons
    st.subheader("🔍 Choose a Model for Prediction:")
    model_choice = st.radio(
        "Select the model you want to use:",
        list(models.keys()),
        index=0  # Default selection
    )

    # User input fields
    st.subheader("📝 Enter Loan Application Details")
    Gender = st.radio('Gender:', ["Male", "Female"], horizontal=True)
    Married = st.radio('Marital Status:', ["Unmarried", "Married"], horizontal=True)
    ApplicantIncome = st.number_input("📊 Applicant's Monthly Income", min_value=0.0, format="%.2f")
    LoanAmount = st.number_input("💰 Total Loan Amount", min_value=0.0, format="%.2f")
    Credit_History = st.radio('📜 Credit History:', ["Unclear Debts", "No Unclear Debts"], horizontal=True)

    result = ""

    # When 'Predict' is clicked, make the prediction using the selected model
    if st.button("🚀 Predict Loan Approval"):
        selected_model = models[model_choice]  # Get the correct model
        result = prediction(selected_model, Gender, Married, ApplicantIncome, LoanAmount, Credit_History)
        st.success(f'Your loan is {result}')

if __name__ == '__main__':
    main()
