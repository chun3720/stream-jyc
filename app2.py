import streamlit as st
# import numpy as np
import pandas as pd
import os
# import matplotlib.pyplot as 

# dummy = "0928 18-61-1 LiP-ECDEC_02_CstC.txt"
# dummy2 = "0928 18-61-1 LiP-ECDEC_02_CstC_cycle_4.csv"
file = st.file_uploader(label="select file ")

def predict():
    
    print(file.name)
    print(type(file))
    name, ext = os.path.splitext(file.name)
    
    if ext == ".txt":
    
    
        df = pd.read_csv(file, sep = "\s", engine = "python")
        
    elif ext == ".csv":
        df = pd.read_csv(file)
    
    # st.success(f"{df.columns}")
    
    x, y = df.columns[0], df.columns[1]
    st.line_chart(df, x = x, y = y)
    st.success(f"{df.columns}")


st.button("Predict", on_click=predict)