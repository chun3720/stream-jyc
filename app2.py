import streamlit as st
import pickle

# import numpy as np
# import pandas as pd
# import os
# from src.supycap import Supycap_obj
# from Supycap import Load_capacitor
# import matplotlib.pyplot as plt
# import numpy as np
import pathlib
import src.utils
import os

# import matplotlib.pyplot as

# dummy = "0928 18-61-1 LiP-ECDEC_02_CstC.txt"
# dummy2 = "0928 18-61-1 LiP-ECDEC_02_CstC_cycle_4.csv"
curr_path = pathlib.Path().resolve()
example_path = os.path.join(curr_path, "example")
choice = st.selectbox("Select to analyze", ("Supercap", "Battery"))
st.write("You selected: ", choice)


#
# import pandas as pd
if choice == "Supercap":
    st.write("available raw data: .mpt file only ")
    st.write("mpt file must include all cycles")
    agree = st.checkbox("See example analysis")
    if agree:
        file = os.path.join(example_path, "supycap.mpt")
        st.button(
            "Supercap analysis",
            on_click=src.utils.supycap,
            kwargs={"file": file, "example": True},
        )
    else:
        file = st.file_uploader(label="select file ")

        st.button(
            "Supercap analysis", on_click=src.utils.supycap, kwargs={"file": file}
        )

elif choice == "Battery":
    agree = st.checkbox("See example analysis")
    if agree:
        file1 = os.path.join(example_path, "Battery_DC.pkl")
        file2 = os.path.join(example_path, "Battery_CYC.csv")
        st.button(
            "Battery analysis",
            on_click=src.utils.battery_cycle,
            kwargs={"files": [file1, file2], "example": True},
        )
    else:
        files = st.file_uploader(
            label="select files (shoud include both DC and CYC file) :",
            accept_multiple_files=True,
        )

        st.button(
            "Specific Capacity vs cycle",
            on_click=src.utils.battery_cycle,
            kwargs={"files": files},
        )
        with open("battery_object.pkl", "rb") as f:
            curve_object = pickle.load(f)

        cycle_list = list(map(str, range(1, len(curve_object) + 1)))

        cycle_choice = st.multiselect(
            "Selet cycle number to display", cycle_list, key="choice"
        )
        st.write("You selected: ", cycle_choice)

        # print(cycle_choice)

        st.button(
            "Battery curve",
            on_click=src.utils.battery_curve,
            kwargs={"choices": cycle_choice},
        )
        # cycle_list = list(map(str, range(len(curve_object))))

        # cycle_choice = st.multiselect("Selet cycle number to display", cycle_list)
        # st.write("You selected: ", cycle_choice)
