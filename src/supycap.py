import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import re
import pathlib

# from loadexp import win2linux
# from io import StringIO
# file = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw\\1117 Supycap test\\0928 18-61-2 LiP-ECDEC_02_CstC.mpt"

# lin_path = win2linux(file)



# @dataclass
class Supycap_obj:
    
    def __init__(self, file):
        self.file = file
        # method_dict = {'Constant Current\n' : "GCD", 'Cyclic Voltammetry\n' : "CV"}
        # self.method = ''
        bytes_data = self.file.getvalue()
        data = self.file.getvalue().decode("utf-8").splitlines()
        h = re.findall('[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', data[1])
        self.header = int(h[0])     
        
        # if self.method == "GCD":
        self.df = pd.read_csv(self.file, skiprows = self.header-1, sep = "\t", header = 0\
                                , usecols = ["time/s", "control/mA", '<Ewe>/V', 'Capacity/mA.h', 'cycle number' ])
        
        # elif self.method == "CV":
        #     self.df = pd.read_csv(self.file, skiprows = self.header-1, sep = "\t", header = 0\
        #                           , usecols = ["time/s", "control/V", "Ewe/V", "<I>/mA", "cycle number"])
                
        self.df.columns = ["Time", "Curr", "Volt", "Cap", "num"]
        
        parent_path = pathlib.Path(__file__).parent.parent.resolve()
        # save_path = os.path.join(parent_path, "data")
        complete_name = os.path.join(parent_path, file.name[:-4] + ".txt")
        
        self.df[["Time", "Volt"]].to_csv(complete_name, index = False, sep = " ")
        
        
        self.exported_file = complete_name
        
        
        # supercap1 = Load_capacitor(complete_name, ESR_method = 2)
        
        # destination_file = open(complete_name, 'w')
        
    def get_info(self):
        
        return self.df.loc[0]["Curr"]
        
    
        
        
        
        
    