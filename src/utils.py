import streamlit as st
from Supycap import Load_capacitor
import matplotlib.pyplot as plt
import numpy as np
from src.supycap import Supycap_obj, Supycap_example
from src.Battery_wonatech import LIB_cyc, LIB_tot, LIB_sep
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def supycap(file, example=False):

    # supycap1 = Supycap_obj(file)

    if example:
        sc1 = Supycap_example(file)
    else:
        sc1 = Supycap_obj(file)

    st.line_chart(sc1.df, x="Time", y="Volt")

    curr = sc1.df.loc[0]["Curr"]

    read_file = sc1.exported_file

    supercap = Load_capacitor(
        read_file, ESR_method=2, current=curr, cap_grav=False, cap_method=1
    )
    fig, ax = plt.subplots()
    fig = supercap.Check_analysis(begin=1, end=len(sc1.cycles) - 1)
    st.set_option("deprecation.showPyplotGlobalUse", False)
    st.pyplot(fig)

    supercap2 = Load_capacitor(
        read_file, ESR_method=2, current=curr, cap_grav=False, cap_method=2
    )
    fig3, ax3 = plt.subplots()
    fig3 = supercap2.Check_analysis(begin=1, end=len(sc1.cycles) - 1)
    st.pyplot(fig3)

    fig2, ax2 = plt.subplots()
    cap_results = np.array(supercap.cap_ls)
    cap_results2 = np.array(supercap2.cap_ls)
    ax2.scatter(
        range(cap_results.shape[0]),
        cap_results * 1000,
        s=20**2,
        marker="o",
        c="r",
        alpha=0.5,
        label="method1: lower half",
    )
    ax2.scatter(
        range(cap_results2.shape[0]),
        cap_results2 * 1000,
        s=20**2,
        marker="o",
        c="b",
        alpha=0.5,
        label="method2: upper half",
    )
    plt.xlabel("number of cycles", fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("Capacitance (mF)", fontsize=20)
    plt.yticks(fontsize=15)
    plt.legend(loc="center", fontsize=20)

    st.pyplot(fig2)


def battery_cycle(files):

    DC = [_ for _ in files if _.name.endswith("DC.csv")][0]
    CYC = [_ for _ in files if _.name.endswith("CYC.csv")][0]

    profile_obj = LIB_tot(DC)
    cycle_obj = LIB_cyc(CYC)

    mass = cycle_obj.raw.mass.iloc[0]
    df = profile_obj.get_separation(mass)
    profile_obj.raw.to_parquet("raw_with_mass.pqt")

    # print1
    # fig, ax = plt.subplots()
    # ax.scatter(df["Cycle"], df["Specific Capacity (Ah/g)"], s = 10**2, alpha = 0.5)
    # plt.xlabel("Cycles", fontsize = 'large')
    # plt.ylabel("Specific Capacity (Ah/g)", fontsize = 'large')
    # st.pyplot(fig)

    fig2 = px.scatter(df, x="Cycle", y="Specific Capacity (Ah/g)")
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    fig2.update_traces(marker_size=10)
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

    # single_curve = curve_object[0]

    # single_obj = LIB_sep(single_curve)
    # single_obj.get_GCD()

    # fig3 = go.Figure()

    # fig3.add_trace(go.Scatter(x = single_obj.df["q_c"]
    #                        ,y = single_obj.df["v_c"]
    #                        ,mode = 'lines'
    #                        ,line = dict(color = 'firebrick', width = 4)
    #                     #    ,color = 'firebrick'
    #                        ))
    # fig3.add_trace(go.Scatter(x = single_obj.df["q_d"]
    #                        ,y = single_obj.df["v_d"]
    #                        ,mode = 'lines'
    #                        ,line = dict(color = 'firebrick', width = 4)
    #                     #    ,color = 'firebrick'
    #                        ))
    # fig3.update_layout(showlegend = False
    #                    ,xaxis_title = dict(text = "Capacity (Ah/g)")
    #                    ,yaxis_title = dict(text = "Voltage (V)")
    #                    )

    # st.plotly_chart(fig3)


def battery_curve():
    df = pd.read_parquet("raw_with_mass.pqt")

    st.write(df.columns)
