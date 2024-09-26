import streamlit as st
import json

# Load the association rules from the JSON file
with open('heart_association_rules.json', 'r') as file:
    association_rules = json.load(file)

# Extract unique antecedents from the rules
def get_unique_antecedents(association_rules):
    antecedents = set()
    for rule in association_rules:
        for item in rule['antecedent']:
            antecedents.add(item.split('_')[0])  # Extract only the base feature name
    return list(antecedents)

unique_antecedents = get_unique_antecedents(association_rules)
# print(unique_antecedents)
# Custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
        background: rgb(0,13,36);background: linear-gradient(354deg, rgba(0,13,36,1) 14%, rgba(9,9,121,1) 45%, rgba(137,23,181,1) 93%);
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            color: white;
        }
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        * {
            font-family: 'Roboto', sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: rgba(0, 0, 0.5, 0.9);
            color: white;
            padding: 20px;
            border-radius: 15px;
        }
        .stSidebar h1, .stSidebar input, .stSidebar select {
            color: white;
        }
        .prediction-box {
            padding: 20px;
            border-radius: 15px;
            background-color: rgba(255, 0, 0, 0.7);
            color: white;
            font-weight: bold;
            font-size: 22px;
            text-align: center;
        }
        button {
            font-size: 18px;
            padding: 12px;
            border-radius: 10px;
            background-color: #0044cc;
            color: white;
            border: none;
        }
        button:hover {
            background-color: #0033a0;
            color: white;
        }
        .input-panel {
            background-color: rgba(0.2,0.2, 0, 0.5);
            padding: 20px;
            border-radius: 15px;
            margin: 0 auto;
            width: 80%;
            max-width: 600px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Pre-process user input (discretize age, cholesterol as needed)
def preprocess_input(user_input):
    processed_input = {key: f"{key}_{user_input[key]}" for key in user_input}
    return processed_input

# Predict using association rules
def predict_disease(user_input, association_rules):
    for rule in association_rules:
        antecedents = rule['antecedent']
        if all(feature in user_input.values() for feature in antecedents):
            return f"Warning: Heart Disease with confidence: {rule['confidence']} and lift: {rule['lift']}", "red"
    return "Good News: No significant indicators of heart disease were found based on the provided input.", "green"

# Streamlit app
def main():
    st.set_page_config(page_title="Heart Disease Prediction", page_icon="❤️", layout="centered")

    add_custom_css()

    st.title("Heart Disease Prediction using Association Rules")

    with st.sidebar:
        st.header("Patient Information")

        # Only display input fields for features present in the rules
        user_input = {}
        if 'age' in unique_antecedents:
            user_input['age'] = st.text_input("Enter age:")
        if 'sex' in unique_antecedents:
            user_input['sex'] = st.selectbox("Enter sex:", ["male", "female"])
        if 'chest pain type' in unique_antecedents:
            user_input['chest pain type'] = st.selectbox("Enter chest pain type:", ["typical angina", "atypical angina", "non-anginal pain", "asymptomatic"])
        if 'exercise angina' in unique_antecedents:
            user_input['exercise angina'] = st.selectbox("Exercise-induced angina?", ["yes", "no"])
        if 'ST slope' in unique_antecedents:
            user_input['ST slope'] = st.selectbox("Enter ST slope:", ["upsloping", "flat", "downsloping"])
        if 'fasting blood sugar' in unique_antecedents:
            user_input['fasting blood sugar'] = st.text_input("Enter fasting blood sugar:")
        if st.button("Predict"):
            # Preprocess input
            processed_input = preprocess_input(user_input)

            # Make prediction
            prediction, color = predict_disease(processed_input, association_rules)

            # Store prediction in session state
            st.session_state['prediction'] = prediction
            st.session_state['color'] = color

    if 'prediction' in st.session_state:
        st.subheader("Prediction Result")
        st.markdown(f"<div class='prediction-box' style='background-color: {st.session_state['color']};'>{st.session_state['prediction']}</div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
