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
   ["Bosh Sahifa", "Kredit Tasdiqlash", "Dori vositalari tavsiyasi", "Avtomobil narxlash", "Noutbokni narxlash"]
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
   age = st.number_input("Yosh:", step=1)
   income = st.number_input("Yillik daromad ($):", step=1)
   loan_amount = st.number_input("Kredit miqdori ($):", step=1)
   credit_score = st.number_input("Kredit reytingi:", step=1)

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
   year = st.number_input("Ishlab chiqarilgan yili", step=1)
   sp = st.number_input("Dvigatel hajmi", step=0.1)
   dk = st.number_input("Yurgan yo'li probeg", step=1)
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
      prediction = model.predict(df)[0]
      st.success(f"{mm} mashinangizning taxminiy narxi: ${prediction:.2f}$ {"$"}")
      
elif menu == "Noutbokni narxlash":
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
   with open('laptopprice.pkl', 'rb') as file:
    model = pickle.load(file)
    
   st.title("Noutbook narxi")
   st.write("Bu dastur sizning kiritgan ma'lumotlaringizga asoslanib noutbokingizni taxminiy narxini bashorat qiladi!")

   mm = st.text_input("Noutbok nomi")
   PrimaryStorageType = st.selectbox("Hotira turi", ["SSD", "HDD",	"Flash Storage", "Hybrid"])
   if PrimaryStorageType=="SSD":
      PrimaryStorageType=3
   elif PrimaryStorageType=="HDD":
      PrimaryStorageType=1
   elif PrimaryStorageType=="Flash Storage":
      PrimaryStorageType=0
   elif PrimaryStorageType=="Hybrid":
      PrimaryStorageType=2
   PrimaryStorage = st.number_input("Hotira (GB)", step=1)
   ram = st.number_input("RAM", step=1)
   Screen = st.selectbox("Ekran sifati", ["Full HD", "Standard", "4K Ultra HD", "Quad HD+"])
   if Screen=="Full HD":
      Screen=1
   elif Screen=="Standard":
      Screen=3
   elif Screen=="4K Ultra HD":
      Screen=0
   elif Screen=="Quad HD+":
      Screen=2
   ScreenW = st.number_input("Ekran kengligi (piksel)", step=1)
   ScreenH = st.number_input("Ekran balandligi (piksel)", step=1)
   CPU_freq = st.number_input("Markaziy protsessor (CPU) tezligi")

      
   if st.button("Bashorat qilish"):
      df =pd.DataFrame([{
         'Ram': ram,
         'Screen': Screen,
         'ScreenW': ScreenW,
         'ScreenH': ScreenH,
         'CPU_freq': CPU_freq,
         'PrimaryStorage': PrimaryStorage,
         'PrimaryStorageType': PrimaryStorageType
      }]) 
      prediction = model.predict(df)[0]
      st.success(f"{mm} noutbokingizni taxminiy narxi: ${prediction:.2f}$ {"$"}")
