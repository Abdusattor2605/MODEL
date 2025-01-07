import streamlit as st
import pickle
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

st.sidebar.header("📊 Ilova Bo'limlari")
menu = st.sidebar.radio(
   "Menyu:",
   ["Bosh Sahifa", "Kredit Tasdiqlash", "Dori vositalari tavsiyasi", "Avtomobil narxlash", "Kvartira narxlash"]
)

if menu == "Bosh Sahifa":
   st.header("**XUSH KELIBSIZ!!!** \nBizning hizmatlarimizdan foydalanayotganizdan mamnunmiz!")
   st.header("Bizning xizmatlarimiz")
   st.markdown("""
   - **Moliyaviy tahlil**: Mijozlarning moliyaviy ahvolini chuqur tahlil qilish.
   - **Dori vositalari tavsiyasi**: Mijozlarning tibbiy holatiga qarab ularga dori tavsiya qilish.
   - **Avtomobil narxlash**: Mijozlarning avtomobil holatiga qarab avtomobilini narxlash.
   - **Kvartira narxlash**: Mijozlarning uylarini sotishda narxlashga yordam berish.
   """)

elif menu == "Kredit Tasdiqlash":
   st.markdown(
    f"""
    <style>
      .stApp {{
        background-color: {'#002352'};
    }}
    </style>
    """,
    unsafe_allow_html=True
   )

   model = joblib.load("bank_model.pkl")

   st.header("Kredit Tasdiqlash")

   st.markdown("Ma'lumotlaringizni kiriting:")
   age = st.number_input("Yosh:", 18, 100, 25)
   income = st.number_input("Yillik daromad ($):", 10000, 1000000, 50000)
   loan_amount = st.number_input("Kredit miqdori ($):", 1000, 500000, 20000)
   credit_score = st.number_input("Kredit reytingi:", 300, 850, 700)

   if st.button("Aniqlash"):
      features = np.array([[age, income, loan_amount, credit_score]])
      prediction = model.predict(features)
      if prediction[0] == 1:
         st.success("Kredit tasdiqlandi!")
      else:
         st.error("Kredit rad etildi.")
         
elif menu == "Dori vositalari tavsiyasi":
   st.markdown(
    f"""
    <style>
      .stApp {{
        background-color: {'#003A52'};
    }}
    </style>
    """,
    unsafe_allow_html=True
   )
   with open('Dori_Tavsiyasi.pkl', 'rb') as file:
      model = pickle.load(file)

   st.title("Dori vositalari tavsiyasi")
   Age = st.number_input("Yosh", min_value=0, max_value=120, value=20)
   sex = st.selectbox("Jins", ["Erkak", "Ayol"])
   if sex=="Ayol":
      Sex=0
   elif sex=="Erkak":
      Sex=1
   bp = st.selectbox("Qon bosimi", ["PAST", "NORMAL", "YUQORI"])
   if bp=="YUQORI":
      BP=0
   elif bp=="PAST":
      BP=1
   elif bp=="NORMAL":
      BP=2
   cholesterol = st.selectbox("Qondagi xolesterol", ["NORMAL", "YUQORI"])
   if cholesterol=="NORMAL":
      Cholesterol=1
   elif cholesterol=="YUQORI":
      Cholesterol=0
   Na_to_k = st.number_input("Organizmdagi natriy miqdorining kaliyga nisbati", min_value=0.0, value=10.0)

   if st.button("Bashorat qilish"):
      input_data = pd.DataFrame([{
         'Age': Age, 
         'Sex': Sex, 
         'BP': BP, 
         'Cholesterol': Cholesterol, 
         'Na_to_k': Na_to_k
      }])
      prediction = model.predict(input_data)[0]
      st.success(f"Tavsiya etilgan dori ${prediction}$")
      
elif menu == "Avtomobil narxlash":
   st.markdown(
    f"""
    <style>
      .stApp {{
        background-color: {'#004352'};
    }}
    </style>
    """,
    unsafe_allow_html=True
   )
   with open('avtonarx.pkl', 'rb') as file:
    model = pickle.load(file)
    
   st.title("AVTO NARX")
   st.write("Bu dastur sizning kiritgan ma'lumotlaringizga asoslanib avtomobilingizning taxminiy narxini bashorat qiladi!")

   mm = st.text_input("Mashina modeli")
   year = st.text_input("Ishlab chiqarilgan yili")
   sp = st.text_input("Dvigatel hajmi")
   dk = st.text_input("Yurgan yo'li probeg")
   ftt = st.selectbox("Yoqilg'i turi", ["Benzin","Gaz","Elektr"])

   if ftt=="Benzin":
      ft=2
   elif ftt=="Gaz":
      ft=0
   elif ftt=="Elektr":
      ft=1
   
   if st.button("Bashorat qilish"):
      df =pd.DataFrame([{
         'year': year,
         'mileage': dk,
         'fuelType': ft,
         'engineSize': sp
      }]) 
      df['year'] = encoder.fit_transform(df['year'].values)
      df['engineSize'] = encoder.fit_transform(df['engineSize'].values)
      df['mileage'] = encoder.fit_transform(df['mileage'].values)
      prediction = model.predict(df)[0]
      st.success(f"{mm} mashinangizning taxminiy narxi: ${prediction:.2f}$ {"$"}")
      
elif menu == "Kvartira narxlash":
   st.markdown(
    f"""
    <style>
      .stApp {{
        background-color: {'#003152'};
    }}
    </style>
    """,
    unsafe_allow_html=True
   )
   with open('uynarx.pkl', 'rb') as f:
      model = pickle.load(f)

   st.title("Uy narxini bashorat qilish")
   bedrooms = st.number_input("Yotoqxonalar soni", min_value=1, step=1)
   bathrooms = st.number_input("Hammomlar soni", min_value=1.0, step=0.5)
   sqft_living = st.number_input("Yashash maydoni", min_value=500, step=50)
   floors = st.number_input("Qavatlar soni", min_value=1.0, step=0.5)
   yr_built = st.number_input("Qurilgan yili", min_value=1900, max_value=2023, step=1)

   if st.button("Narxni bashorat qilish"):
      input_data = pd.DataFrame({
         'bedrooms': [bedrooms],
         'bathrooms': [bathrooms],
         'sqft_living': [sqft_living],
         'floors': [floors],
         'yr_built': [yr_built]
      })
      prediction = model.predict(input_data)
      st.success(f"Bashorat qilingan narx: ${prediction[0]:,.2f}")
