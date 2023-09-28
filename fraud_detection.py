import streamlit as st
import pandas as pd
# import seaborn as sns
import matplotlib as plt
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')
import joblib
import pickle
import time
# import bcrypt  # For password hashing
# import re  # For regular expressions

#load the model
model = pickle.load(open('online_fraud_detection.pkl', 'rb'))

# Function for data preprocessing
def preprocess_data(data):
    # Create a DataFrame from the user input
    input_data = pd.DataFrame([data])

#add picture from local computer
import base64 
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('Untitled.jpeg') 

# Define a regular expression pattern to enforce the password criteria
# password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}$"

# # Simulated user database
# users = {
#     'Taiwo': {
#         'password_hash': bcrypt.hashpw(b'mypassword', bcrypt.gensalt())
#     },
#     'Ehiz': {
#             'password_hash': bcrypt.hashpw(b'mypassword', bcrypt.gensalt())
#         },
#     'Danny': {
#             'password_hash': bcrypt.hashpw(b'mypassword', bcrypt.gensalt())
#         }      

# }

# def authenticate_user(username, password):
#     user_data = users.get(username)
#     if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password_hash']):
#         return True
#     return False

# # Initialize the logged_in variable
# logged_in = False

# # Only show the login form if not logged in
# if not logged_in:
#     st.title("User Login")
#     username = st.text_input('Username')
#     password = st.text_input('Password', type='password')

#     if st.button('Login'):
#         if authenticate_user(username, password):
#             st.success('Login Successful')
#             logged_in = True
#         else:
#             st.error('Login Failed. Please check your credentials')

# # Only show the content if the user is logged in
# if logged_in:
#     # Import CSS file into Streamlit
with open('fraud_detection.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 style = 'top-margin: 0rem;text-align: center; color: #252B48;'>ONLINE PAYMENT FRAUD DETECTION</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='font-weight: bold; font-style: italic; font-family: Optima; color: #F5F5DC'>built by TAIWO K. LASH</h6>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("<h4 style='font-weight: bold; colour: #E55604'>Overview</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: justify; color: #F5FCCD; background-color: #252B48; padding: 10px;'>Online payment fraud is a significant concern for financial institutions, e-commerce platforms, and consumers. Fraudsters continually devise new methods to exploit vulnerabilities in online payment systems, resulting in financial losses and security breaches. This application is built to identify online payment fraud swiftly and prevent fraudulent transactions in real-time.</p>", unsafe_allow_html=True)

    # data = pd.read_csv('onlinefraud.csv')
df = pd.read_csv('column explanation.txt')
    # df.reset_index(drop=True, inplace=True)

custom_css = """
    <style>
        .st-af {
            color: black !important;
        }
    </style>
    """
st.markdown(custom_css, unsafe_allow_html=True)

with st.form('my_form', clear_on_submit=True):
    st.header("FRAUD DETECTION")
    with st.expander("Variable Definitions"):
        st.table(df)
    Type_of_Transaction = st.selectbox('Type of Transaction', ['', 'CASH_OUT', 'PAYMENT', 'CASH_IN', 'TRANSFER', 'DEBIT'])
    Amount = float(st.number_input('Amount'))
    Balance_Before_Transaction = float(st.number_input('Balance Before Transaction'))
    Balance_After_Transaction = float(st.number_input('Balance After Transaction'))
    Recipients_Old_Balance = float(st.number_input("Recipient Old Balance"))
    Recipients_New_Balance = float(st.number_input("Recipient New Balance"))
    
    submitted = st.form_submit_button("SUBMIT")   
    if (Type_of_Transaction and Amount and Balance_Before_Transaction and Balance_After_Transaction and Recipients_Old_Balance and Recipients_New_Balance):
        if submitted:
            with st.spinner(text='Loading..'):
                # time.sleep(1)
                st.write("Your Inputted Data:")           

                input_var = pd.DataFrame([{'type' : Type_of_Transaction, 'amount' : Amount, 'oldbalanceOrg' : Balance_Before_Transaction, 'newbalanceOrig' : Balance_After_Transaction, 'oldbalanceDest' : Recipients_Old_Balance, 'newbalanceDest' : Recipients_New_Balance}])
                st.write(input_var) 
                    
                from sklearn.preprocessing import LabelEncoder, StandardScaler
                lb = LabelEncoder()
                scaler = StandardScaler()
                for i in input_var:
                    if input_var[i].dtypes == 'int' or input_var[i].dtypes == 'float':
                        input_var[[i]] = scaler.fit_transform(input_var[[i]])
                    else:
                        input_var[i] = lb.fit_transform(input_var[i])
                

                # time.sleep(2)
                prediction = model.predict(input_var)
                
                if prediction == 0:
                    st.error('Transaction is not fraudulent')
                else:
                    # st.balloons()
                    st.success('Transaction is fraudulent')
                # st.write(prediction)

