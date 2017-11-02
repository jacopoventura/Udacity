# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 18:31:25 2017

@author: jacopo
"""

# import SQLIte3
import sqlite3
import numpy as np

# function for query
def query_db(QUERY,cursor):
    cursor.execute(QUERY)
    results = cursor.fetchall()
    
    # print
    size = np.shape(results)
    if size[1]==1:
        for r in results:
            print(r[0])
    else:
        for r in results:
            name = str(r[0])
            name = name[2:]
            print(str(name[:-1]) + ': ' + str(r[1]))
    