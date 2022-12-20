import streamlit as st
# import numpy as np
import pandas as pd
import os
from src.supycap import Supycap_obj
from Supycap import Load_capacitor
import matplotlib.pyplot as plt
import numpy as np


# import matplotlib.pyplot as 

# dummy = "0928 18-61-1 LiP-ECDEC_02_CstC.txt"
# dummy2 = "0928 18-61-1 LiP-ECDEC_02_CstC_cycle_4.csv"
file = st.file_uploader(label="select file ")

def predict():
    
    # supycap1 = Supycap_obj(file)
    
    sc1 = Supycap_obj(file)
    
    curr = sc1.df.loc[0]["Curr"]
    
    read_file = sc1.exported_file
    
    supercap = Load_capacitor(read_file, ESR_method=2, current = curr, cap_grav =  False, cap_method =2)
    fig, ax = plt.subplots()
    fig = supercap.Check_analysis(begin =1, end = 3)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)
    
    fig2, ax2 = plt.subplots()
    cap_results = np.array(supercap.cap_ls)
    ax2.scatter(range(cap_results.shape[0]), cap_results*1000, marker = 'o', c = "r")
    plt.xlabel("number of cycles")
    plt.ylabel("Capacitance (mF)")
    st.pyplot(fig2)
    
    
    
    
    st.line_chart(sc1.df, x = "Time", y = "Volt")
    
    # 
    


st.button("Predict", on_click=predict)