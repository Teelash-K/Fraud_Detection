import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib as plt
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')
import joblib
import pickle
import time


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

# to import css file into streamlit
with open('fraud_detection.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)


st.markdown("<h4>ONLINE PAYMENT FRAUD DETECTION</h4>", unsafe_allow_html=True)
st.markdown("<p style = 'font-weight: bold; font-style: italic; font-family: Optima;  color: #FF9B82'>built by TAIWO K. LASH</h1>", unsafe_allow_html = True)
st.markdown("<br><br>", unsafe_allow_html = True) 


st.markdown("<h3>Overview</h3>", unsafe_allow_html = True)

st.markdown("<p style = 'color : #191717'>Online payment fraud is a significant concern for financial institutions, e-commerce platforms, and consumers. Fraudsters continually devise new methods to exploit vulnerabilities in online payment systems, resulting in financial losses and security breaches. This application is built to identify online payment fraud swiftly and prevent fraudulent transactions in real-time.</p>", unsafe_allow_html=True)


data = pd.read_csv('onlinefraud.csv')
df = pd.read_csv('column explanation.txt')
df.reset_index(drop=True, inplace=True)
# df.drop('Unnamed: 1', inplace = True, axis = 1)


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
    Amount = float(st.number_input('Amount', value=0.0))
    Customer_Name = st.text_input('Customer Name',['', 'C1231006815', 'C1231006845', 'C1231076415'])
    Balance_Before_Transaction = float(st.number_input('Balance Before Transaction', value = 0.0))
    Balance_After_Transaction = float(st.number_input('Balance After Transaction',value=0.0))
    Recipient_Name = st.text_input('Recipient Name')
    Recipients_Old_Balance = float(st.number_input("Recipient Old Balance", value=0.0))
    Recipients_New_Balance = float(st.number_input("Recipient New Balance", value=0.0))
    Number_of_step = int(st.number_input("Number of Step", value=0))

    
    submitted = st.form_submit_button("SUBMIT")   
    if (Type_of_Transaction and Amount and Customer_Name and Balance_Before_Transaction and Balance_After_Transaction and Recipient_Name and Recipients_Old_Balance and Recipients_New_Balance and Number_of_step):
        if submitted:
            with st.spinner(text='Loading..'):
                time.sleep(1)
                st.write("Your Inputted Data:")           

                input_var = pd.DataFrame([{'type' : Type_of_Transaction, 'amount' : Amount, 'nameOrig' : Customer_Name, 'oldbalanceOrg' : Balance_Before_Transaction, 'newbalanceOrig' : Balance_After_Transaction, 'nameDest' : Recipient_Name, 'oldbalanceDest' : Recipients_Old_Balance, 'newbalanceDest' : Recipients_New_Balance, 'step' : Number_of_step}])
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