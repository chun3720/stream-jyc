from galvani import BioLogic
# from loadexp import win2linux
import pandas as pd


#LSV.py
# raw = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1228 18-55-4 ORR\ORR and OER_01_LSV.mpr"

# file = win2linux(raw)


# mpr_file = BioLogic.MPRfile(str(file))

# df = pd.DataFrame(mpr_file.data)

class LSV_curve:
    def __init__(self, file):
    
        mpr_file = BioLogic.MPRfile(file)
        
        self.df = pd.DataFrame(mpr_file.data)
