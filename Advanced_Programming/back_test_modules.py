# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 22:17:29 2023

@author: jwkim
"""
import pandas as pd
import numpy as np

def index_100(ret_df):
    index_df = (1 + ret_df).cumprod() * 100
    
    return index_df

def ret_risk_profile(mp_index):
    ret_df = pd.DataFrame(index=mp_index.columns)
    ret_df["누적수익률"] = mp_index.iloc[-1] / mp_index.iloc[0] - 1
    delta_to_years = (mp_index.index[-1] - mp_index.index[0]).days / 365.25
    ret_df["누적수익률(연율화)"] = (1 + ret_df["누적수익률"]) ** (1 / delta_to_years) - 1
    ret_df["변동성(연율화)"] = mp_index.resample("W").last().pct_change().std() * np.sqrt(52)
    ret_df = ret_df * 100
    ret_df["샤프비율"] = ret_df["누적수익률(연율화)"] / ret_df["변동성(연율화)"]
    index_year = mp_index.resample("A").last()
    index_year_pct = index_year.pct_change()
    index_year_pct.iloc[0] = index_year.iloc[0] / 100 - 1
    index_year_pct.index = index_year_pct.index.year
    index_year_pct = index_year_pct * 100
    
    ret_df["음의 변동성(연율화)"] = mp_index.resample("W").last().pct_change() [mp_index.resample("W").last().pct_change()<0 ].std() * np.sqrt(52)
    ret_df["Sortino"] = ret_df["누적수익률(연율화)"] / ret_df["음의 변동성(연율화)"]
    
    comp_ret = (mp_index.pct_change()+1).cumprod() 
    peak=comp_ret.expanding(min_periods=1).max() 
    dd = (comp_ret/peak)-1 
    ret_df["Maxdrawdown"] =dd.min() 

    return pd.concat([ret_df.T, index_year_pct])