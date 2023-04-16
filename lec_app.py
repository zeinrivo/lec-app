import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd 
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


# import dataset
dataset = pd.read_csv("loan_data_set.csv") 

# replace Null values with a specified value
dataset['Gender']=dataset['Gender'].fillna(dataset['Gender'].mode().values[0])
dataset['Married']=dataset['Married'].fillna(dataset['Married'].mode().values[0])
dataset['Dependents']=dataset['Dependents'].fillna(dataset['Dependents'].mode().values[0])
dataset['Self_Employed']=dataset['Self_Employed'].fillna(dataset['Self_Employed'].mode().values[0])
dataset['LoanAmount']=dataset['LoanAmount'].fillna(dataset['LoanAmount'].mean())
dataset['Loan_Amount_Term']=dataset['Loan_Amount_Term'].fillna(dataset['Loan_Amount_Term'].mode().values[0] )
dataset['Credit_History']=dataset['Credit_History'].fillna(dataset['Credit_History'].mode().values[0] )

# drop unimportant column
dataset.drop('Loan_ID', axis=1, inplace=True)

# categorical data to numerical data
gender = {"Female": 0, "Male": 1}
yes_no = {'No' : 0,'Yes' : 1}
dependents = {'0':0,'1':1,'2':2,'3+':3}
education = {'Not Graduate' : 0, 'Graduate' : 1}
property = {'Semiurban' : 0, 'Urban' : 1,'Rural' : 2}
output = {"N": 0, "Y": 1}

# replace categorical data with numerical data 
dataset['Gender'] = dataset['Gender'].replace(gender)
dataset['Married'] = dataset['Married'].replace(yes_no)
dataset['Dependents'] = dataset['Dependents'].replace(dependents)
dataset['Education'] = dataset['Education'].replace(education)
dataset['Self_Employed'] = dataset['Self_Employed'].replace(yes_no)
dataset['Property_Area'] = dataset['Property_Area'].replace(property)
dataset['Loan_Status'] = dataset['Loan_Status'].replace(output)

# independent and dependent variable
x = dataset.drop('Loan_Status', axis = 1)
y = dataset.Loan_Status

# splitting dataset
X_train, X_test, Y_train, Y_test= train_test_split(x, y, test_size= 0.25, random_state=0)

# train the model
knn = KNeighborsClassifier(n_neighbors = 17)
knn.fit(X_train, Y_train)

# web title
st.set_page_config(
    page_title="LEC-App",
)

# navigation/option
with st.sidebar:
   selected = option_menu(
        menu_title="Main Menu",  
        options=["Home", "Demo"], 
        icons=["house", "record-circle"],  
        menu_icon="cast",  # optional
        default_index=0,  # optional         
)

# option : Home
if selected == "Home":
    st.write("# Loan Eligibility Checking App")
    st.write(
    """
    Built with distanced-based supervised machine learning algorithm  \n for classification problem called **K-Nearest Neighbors**.
    """
    )

    image1 = Image.open('knn2.jpg')
    st.image(image1)
    
    st.markdown(
    """
    - [Source Code](https://github.com/zeinrivo/lec-app)
    """
    )
    
    st.caption("Created by **Zein Rivo**")

# option : Demo 
if selected == "Demo":
    st.title("Loan Eligibility Checking App")
    st.write("Customize the input below with your personal data")

    gendeR = {"Male","Female"}
    marrieD = {"Yes","No"}
    dependentS = {"0","1","2","3+"}
    educatioN = {"Graduate","Not Graduate"}
    self_employeD = {"Yes","No"}
    cre_historY = {"Yes","No"}
    propertY = {'Semiurban', 'Urban','Rural'}

    genderr = st.selectbox("Gender",gendeR)
    marriedd = st.selectbox("Married",marrieD)
    dependentss = st.selectbox("Dependents",dependentS)
    educationn = st.selectbox("Education",educatioN)
    self_employedd = st.selectbox("Self-Employed",self_employeD)
    incomee = st.number_input("Income")
    coincomee = st.number_input("Co-Income")
    loan_amountt = st.number_input("Loan Amount")
    loan_amount_termm = st.number_input("Loan Amount Term")
    cre_historyy = st.selectbox("Credit History",cre_historY)
    propertyy = st.selectbox("Property Area",propertY)

    if genderr == "Male":
      genderr = 1
    elif genderr == "Female":
      genderr = 0

    if marriedd == "Yes":
      marriedd = 1
    elif marriedd == "No":
      marriedd = 0

    if dependentss == "0":
      dependentss = 0
    elif dependentss == "1": 
      dependentss = 1
    elif dependentss == "2": 
      dependentss = 2
    elif dependentss == "3+": 
      dependentss = 3

    if educationn == "Graduate":
      educationn = 1
    if educationn == "Not Graduate":
      educationn = 0

    if self_employedd == "Yes":
      self_employedd = 1
    elif self_employedd == "No":
      self_employedd = 0

    if cre_historyy == "Yes":
      cre_historyy = 1
    elif cre_historyy == "No":
      cre_historyy = 0

    if propertyy == "Semiurban":
      propertyy = 0
    elif propertyy == "Urban": 
      propertyy = 1
    elif propertyy == "Rural": 
      propertyy = 2


    ok = st.button ("Check Eligibility")

    if ok:
      x_new = [[genderr,marriedd,dependentss,educationn,self_employedd,incomee,coincomee,loan_amountt,loan_amount_termm,cre_historyy,propertyy]]
      lep = knn.predict(x_new)
      if lep == 0:
        st.subheader("Not Eligible")
      if lep == 1:
        st.subheader("Eligible")
