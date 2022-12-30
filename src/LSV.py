from galvani import BioLogic
import pandas as pd
import os
# from loadexp import win2linux



# raw = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1228 18-55-4 ORR\ORR and OER_01_LSV.mpr"

# file = win2linux(raw)


# mpr_file = BioLogic.MPRfile(str(file))

# df = pd.DataFrame(mpr_file.data)

class LSV_curve:
    def __init__(self, file):
    
        mpr_file = BioLogic.MPRfile(file)
        
        self.df = pd.DataFrame(mpr_file.data)
        # self.name, self.ext = os.path.splitext(os.path.basename(file))
        self.name, self.ext = os.path.splitext(file.name)
