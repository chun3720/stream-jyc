# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:15:23 2021
last update : Feb 15 2022
@author: jycheon
"""

import os
from dataclasses import dataclass
from typing import List
from pathlib import Path, PureWindowsPath
import pandas as pd
from collections import defaultdict


@dataclass
class Dataloads:
    
    path : str
    file : str = None
    
    def __post_init__(self):
        
        if self.file is None:
            
            self.file_path = self.path
            self.path = self.file_path.parent
            self.name, self.ext = self.file_path.stem, self.file_path.suffix
            
        else:
            self.path_obj = Path(self.path)
            # self.file_path = self.path_obj.joinpath(self.file)
            self.file_path = self.path_obj.joinpath(self.file)
            self.name, self.ext = os.path.splitext(self.file)



        
def build_data(path: str, file: List[str], builder: object, err_skip = True):
    "Build class of each file and return list of builded classes"
    data = []
    
    
    if not err_skip:
        
        for item in file:
            
            data.append(builder(path, item))
    
    else:    
        for item in file:
        
            try:
                data.append(builder(path, item))
            except:
                print(f'fail to load <{item}> file')
                pass
        
    
    return data


def build_data2(path: str, files: List[str], builder: object, err_skip = True):
    
    hashmap = defaultdict(builder)
    
    if not err_skip:
        for file in files:
            hashmap[file] = builder(path, file)
            
    return hashmap
    
# from datetime import datetime

# print(datetime.now().isoformat(timespec = 'minutes'))


def win2linux(path):
    # switch = {"C:\\" : "/mnt/c", "D:\\" : "/mnt/d"}  

    winpath = PureWindowsPath(path)
    p_elements = list(winpath.parts)
    # p_elements[0] = switch[p_elements[0]]
    p_elements[0] = "/mnt/" + p_elements[0][0].lower()
    linux_path = "/".join(p_elements)
    
    res_path = Path(linux_path)
    
    return res_path