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
import bcrypt  # For password hashing
import re  # For regular expressions

#load the model
model = pickle.load(open('online_fraud_detection.pkl', 'rb'))


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
add_bg_from_local('online-4533485_640.jpg') 

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

    st.markdown("<h2>ONLINE PAYMENT FRAUD DETECTION</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-weight: bold; font-style: italic; font-family: Optima; color: #FF9B82'>built by TAIWO K. LASH</p>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("<h4>Overview</h4>", unsafe_allow_html=True)

    st.markdown("<p style='color: #191717'>Online payment fraud is a significant concern for financial institutions, e-commerce platforms, and consumers. Fraudsters continually devise new methods to exploit vulnerabilities in online payment systems, resulting in financial losses and security breaches. This application is built to identify online payment fraud swiftly and prevent fraudulent transactions in real-time.</p>", unsafe_allow_html=True)

    data = pd.read_csv('onlinefraud.csv')
    df = pd.read_csv('column explanation.txt')
    df.reset_index(drop=True, inplace=True)

    custom_css = """
    <style>
        .st-af {
            color: white !important;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

with st.form('my_form', clear_on_submit=True):
    st.header("FRAUD DETECTION")
    with st.expander("Variable Definitions"):
            st.table(df)
    Type = st.selectbox('Type', ['', 'CASH_OUT', 'PAYMENT', 'CASH_IN', 'TRANSFER', 'DEBIT'])
    Amount = st.number_input('Amount', min_value=0.0, value=0.0, step=1.0, key="amount")
    NameOrig = st.text_input('Customer Name', key="name_orig")
    OldbalanceOrig = st.number_input('Balance Before Transaction', min_value=0.0, value=0.0, step=1.0, key="old_balance_orig")
    NewbalanceOrig = st.number_input('Balance After Transaction', min_value=0.0, value=0.0, step=1.0, key="new_balance_orig")
    NameDest = st.text_input('Recipient Name', key="name_dest")
    OldbalanceDest = st.number_input("Recipient's Old Balance", min_value=0.0, value=0.0, step=1.0, key="old_balance_dest")
    NewbalanceDest = st.number_input("Recipient's Old Balance", min_value=0.0, value=0.0, step=1.0, key="new_balance_dest")
    Step = st.number_input("Step", min_value=0, value=0, step=1, key = "step")

    submitted = st.form_submit_button("SUBMIT")   
    if (Type and Amount and NameOrig and OldbalanceOrig and NewbalanceOrig and NameDest and OldbalanceDest and NewbalanceDest and Step):
        if submitted:
            with st.spinner(text='Loading..'):
                time.sleep(1)
                st.write("Your Inputted Data:")           

                input_var = pd.DataFrame([{'type' : Type, 'amount' : Amount, 'nameOrig' : NameOrig, 'oldbalanceOrig' : OldbalanceOrig, 'newbalanceOrig' : NewbalanceOrig, 'nameDest' : NameDest, 'oldbalanceDest' : OldbalanceDest, 'newbalanceDest' : NewbalanceDest,  'step' : Step,}])
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
                    st.error('Transaction is not fraudlent')
                else:
                    st.balloons
                    st.success('Transaction is fraudulent')
                # st.write(prediction)
