#%%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math

plt.rcParams['font.family'] ='AppleGothic'
plt.rcParams['axes.unicode_minus'] =False
plt.style.use('seaborn-v0_8-darkgrid')

folder_dir = '/Users/yeomsangyoon/Desktop/2023-2/심화프로그래밍/DATA'
DATA_FILE = "kSE수정주가.xlsx"      # 2000년 1월 2일 ~~~

data_wb = pd.ExcelFile(folder_dir + "/" + DATA_FILE)        
adj_ts = data_wb.parse("Sheet1", index_col=0)

cprice=adj_ts.dropna(axis=1)
cprice.shape
cprice.head()

mprice= cprice.resample('M').mean()
mprice.shape

m_rate=mprice.shift(1)/mprice.shift(11)-1
m_rate.rolling(60).std()
r_monthly=m_rate.dropna(axis=0)
r_monthly.head()

r_monthly.index = r_monthly.index.strftime('%Y-%m')# 그룹별 종목 리스트와 성과분석

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


#  모멘텀에 따른 포트폴리오 구성 

# 시뮬레이션 기간 설정+ 리밸런싱 시점 + 그룹명+ 데이터 프레임 생성 -수익률 채워넣기

start_date = datetime.strptime("2006-01", "%Y-%m")  
end_date = datetime.strptime("2023-09", "%Y-%m")
rebalancing_list = pd.date_range(start_date, end_date, freq='Q').strftime('%Y-%m')   # 리밸런싱 주기(분기) 데이터 생성 (연/월 형식)

column_list = ['top 30%','Bottom 30%']
portfolio_ret_df = pd.DataFrame(columns=column_list, index = cprice.loc[rebalancing_list[0]:].index) #  포트폴리오 일간 수익률 저장


for i in range(len(rebalancing_list)):     # 리밸런싱 날짜에  연간 수익률의 플러스, 마이너스에  따라 종목분류 저장
  
    ym = r_monthly[r_monthly.index==rebalancing_list[i]].squeeze() # 시리즈로 변환
    ym=ym.sort_values()
   
    ps=ym[(ym>=np.quantile(ym,0.7))&(ym>0 )]     # 상위 30%이내 + 양의 모멘텀    ps=ym[(ym>=np.quantile(ym,0.7))&(ym>0 )]  
    plus_momentum_list =ps.index               # 종목명 인덱스
    mn=ym[(ym<=np.quantile(ym,0.3))&(ym<0)]    # 하위 30% 이하 + 음의 모멘텀   ym[(ym<=np.quantile(ym,0.3))&(ym<0)]
    minus_momentum_list = mn.index            # 종목명 인덱스
    
   #  print( plus_momentum_list)
      
### 포트폴리오 일간수익률    :  플러스,마이너스 종목군들을 주가 데이터 날짜에 매칭하여   각 종목군별 일간 주가 수익률 평균 구해 저장
    
    portfolio_ret_df['top 30%'].loc[rebalancing_list[i]:]= cprice[plus_momentum_list].loc[rebalancing_list[i]:].pct_change(1).mean(axis=1).dropna()
    portfolio_ret_df['Bottom 30%'].loc[rebalancing_list[i]:]= cprice[minus_momentum_list].loc[rebalancing_list[i]:].pct_change(1).mean(axis=1).dropna()

   #  일자별 종목군별 (양,음 모멘텀)평균수익률 시계열 데이터 구축

#  이하에서는 해당 시계열을 통해 누적수익률 등 성과평가 측정치 도출

   
portfolio_ret_df.iloc[0] = 0
portfolio_ret_df = portfolio_ret_df.dropna()


plot_list = ['top 30%','Bottom 30%' ]

index_100(portfolio_ret_df[plot_list]).plot()  # 누적수익률 시계열

pp=ret_risk_profile(index_100(portfolio_ret_df[plot_list])) # 성과평가 결과

index_year=index_100(portfolio_ret_df[plot_list]).resample("A").last()  # 연간주기로 변경

print(pp.round(2),end='\n')

index_year.plot()



# %%
