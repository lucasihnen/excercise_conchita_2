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
    "Random Forest": random_forest,
    "Logistic Regression": logistic_regression,
    "SVM": svm
}

# Streamlit cache for efficient processing
@st.cache_data()
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

    # Dropdown to select the model
    model_choice = st.selectbox("Choose a Model", list(models.keys()))

    # User input fields
    Gender = st.selectbox('Gender', ("Male", "Female"))
    Married = st.selectbox('Marital Status', ("Unmarried", "Married"))
    ApplicantIncome = st.number_input("Applicants monthly income", min_value=0.0, format="%.2f")
    LoanAmount = st.number_input("Total loan amount", min_value=0.0, format="%.2f")
    Credit_History = st.selectbox('Credit History', ("Unclear Debts", "No Unclear Debts"))

    result = ""

    # When 'Predict' is clicked, make the prediction using the selected model
    if st.button("Predict"):
        selected_model = models[model_choice]  # Get the correct model
        result = prediction(selected_model, Gender, Married, ApplicantIncome, LoanAmount, Credit_History)
        st.success(f'Your loan is {result}')

if __name__ == '__main__':
    main()
