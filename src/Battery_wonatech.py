import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


class LIB_cyc:
    def __init__(self, CYC):
        self.file = CYC
        self.raw = pd.read_csv(self.file, skiprows= 10, delimiter = ',', encoding = "cp949", index_col = 0, usecols = ["Index", "Cycle_No.", "Dischg.Q(Ah)", 'Dischg.Q_s(Ah/g)'])
        self.raw.columns = ["num", "Q", "Q_s"]
        self.raw["mass"] = self.raw.Q/self.raw.Q_s
        
        
class LIB_tot:   
    
    def __init__(self, DC):       
        self.file = DC
        self.raw = pd.read_csv(self.file, skiprows= 10, delimiter = ',', encoding = "cp949", index_col = 0, usecols = ["Index", "Cycle_No.", "Step_No.", 'Voltage(V)', '|Q|(Ah)'])
        self.raw.columns = ["num", "step", "volt", "cap"]
        self.cycle_tot = len(self.raw.groupby("num"))
        
    def get_separation(self, mass):
        self.raw["cap"] = self.raw["cap"] / mass
        # output_path = os.path.join(self.path, "split")
        # if not os.path.exists(output_path):
        #     os.mkdir(output_path)
        curve_object = []
        idx, caps = [], []
        for i in range(self.cycle_tot):
            j = i + 1
            cy = self.raw[self.raw.num == j]
            curve_object.append(cy)
            # pqt2export = os.path.join(output_path, f"cycle_{j}.pqt")
            # cy.to_parquet(pqt2export)
            steps = cy.step.unique()

            
            non_rest_steps = []
            
            for s in steps:
                check_point = cy[cy.step == s].index[-1]
                cap_at_check_point = cy.cap.loc[check_point]
                
                if cap_at_check_point != 0:
                    non_rest_steps.append(s)
            
                # print(non_rest_steps)
            try:
                if len(non_rest_steps) == 3:
                    c_step, cv_step, d_step = non_rest_steps
                else:
                    c_step, d_step = non_rest_steps
                
                # c_step, d_step = non_rest_steps
                # print(steps)
                # dc_point = cy[cy.step == steps[2]].index[-1] if len(steps) == 4 else cy[cy.step == steps[3]].index[-1]
                dc_point = cy[cy.step ==d_step].index[-1]
                idx.append(j)
                caps.append(cy.cap.loc[dc_point])
            except:
                print(f"Error! Skip {j}th cycle and the thereafter data ")
                pass
            
        d = {"Cycle": idx, "Specific Capacity (Ah/g)" : np.array(caps)}
        df1 = pd.DataFrame(data = d, index = idx)      
        
        return (df1, curve_object)



            
            
class LIB_sep:
    
    def __init__(self, curve):
        self.raw = curve
#         Dataloads.__init__(self, path, file)
#         self.raw = pd.read_parquet(self.file_path)
#         # self.col_name = ["num", "step", "volt", "cap"]
        
    def get_steps(self):
        step_list = self.raw.step.unique()
        non_rest_steps = []
        
        for s in step_list:
            check_point = self.raw[self.raw.step == s].index[-1]
            cap_at_check_point = self.raw.cap.loc[check_point]
            
            if cap_at_check_point != 0:
                non_rest_steps.append(s)
                
        if len(non_rest_steps) == 3:
            c_step, cv_step, d_step = non_rest_steps
        else:
            c_step, d_step = non_rest_steps
            cv_step = None
            
        return (c_step, d_step, cv_step)
        
    def get_GCD(self):
        
        charge_step, discharge_step, cv_step = self.get_steps()
        # steps = self.raw.step.unique()
        cols = ["cap", "volt"]
        
        if cv_step is None:
            self.df = pd.concat([self.raw[self.raw.step == charge_step][cols].reset_index(drop = True),  \
                                 self.raw[self.raw.step == discharge_step][cols].reset_index(drop = True)], \
                                axis =1, ignore_index = True)
                
        else:
            charge_with_cv = pd.concat([self.raw[self.raw.step == charge_step][cols], \
                                        self.raw[self.raw.step == cv_step][cols]] \
                                        
                                        
                                        )
       
            discharge = self.raw[self.raw.step == discharge_step][cols].reset_index(drop = True)
            
            discharge_cap = discharge.cap.max()
            
            # print(discharge_cap)
            
            charge_with_floor = charge_with_cv[charge_with_cv.cap < discharge_cap]
            
            # print(charge_with_floor[cols])
            # print(charge_with_cv)
            
            
            self.df = pd.concat([charge_with_floor[cols].reset_index(drop = True),  \
                                 
                                 self.raw[self.raw.step == discharge_step][cols].reset_index(drop = True)], \
                                axis =1, ignore_index = True)
            
            
            #original
            # self.df = pd.concat([charge_with_cv[cols].reset_index(drop = True),  \
                                 
            #                      self.raw[self.raw.step == discharge_step][cols].reset_index(drop = True)], \
            #                     axis =1, ignore_index = True)
        self.df.columns = ["q_c", "v_c", "q_d", "v_d"]
        
        
    def get_curve(self, color):
        qc, vc, qd, vd = self.df.columns
        plt.plot(self.df[qc], self.df[vc], color, label = self.name)
        plt.plot(self.df[qd], self.df[vd], color)