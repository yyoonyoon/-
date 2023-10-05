#%%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import os
from dateutil.relativedelta import relativedelta

#모듈 임포트 안돼서 그냥 여기에 정의---------
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
#----------------

plt.style.use('seaborn-v0_8-darkgrid')

# 아래 코드 두 줄은 윈도우용 코드 이므로 맥용 코드로 대체 하겠습니다.
# FONT_NAME = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
# rc('font', family=FONT_NAME)
plt.rcParams['font.family'] ='AppleGothic'
plt.rcParams['axes.unicode_minus'] =False
# print(os.getcwd())

# folder_dir: 엑셀 파일이 위치한 폴더 경로
# DATA_FILE: 엑셀 파일의 이름
folder_dir = '/Users/yeomsangyoon/Desktop/2023-2/심화프로그래밍'
DATA_FILE = "KRX300_FIN_DATA_INDEX2023.xlsx"

# pd.ExcelFile() 함수를 사용하여 엑셀 파일을 열기
data_wb = pd.ExcelFile(folder_dir + "/" + DATA_FILE)

# find_ts라는 새로운 데이터프레임에 재무시트를 읽어와서 저장
find_ts = data_wb.parse("재무", index_col=3)  # 인덱스는 연도
adj_close_ts = data_wb.parse("수정주가", header=[1], index_col=0)
adj_close_ts.head(5)
#자기자본 정의
find_ts['자기자본'] = find_ts['총자본'] - find_ts['총부채']


#ROE 정의
find_ts['ROE'] = (find_ts['당기순이익'] / find_ts['자기자본']) * 100

#ROA 정의
find_ts['ROA'] = (find_ts['당기순이익'] / find_ts['총자산']) * 100


#날짜 범위 설정
start_date = 2010
end_date = 2023
filtered_find_ts = find_ts[(find_ts.index >= start_date) & (find_ts.index <= end_date)]

#수익성, 안정성, 성장성 대표적인 지표 하나씩 사용할 예정
# find_ts['ROE']=find_ts ['당기순이익']/find_ts["총자본"]
# find_ts['부채비율']=find_ts ['총부채']/find_ts["총자본"]
# find_ts['영업이익 증가율'] = (find_ts['영업이익'] - find_ts['영업이익'].shift(1)) / find_ts['영업이익'].shift(1) *100

find_ts.head(3)
adj_close_ts.head(3)

# 3번째 헤더 컬럼명 기준으로 데이터 정리
# ps_ts= find_ts[['매출액','영업이익']]    
# print(ps_ts.head(3))

# 재무비율 
find_ts ['ROE']=find_ts ['당기순이익']/find_ts["총자본"]
find_ts ['ROA']=find_ts ['당기순이익']/find_ts["총자산"]
find_ts ['부채비율']=find_ts ['총부채']/find_ts["총자본"]

ps_ts= find_ts[['매출액','영업이익','당기순이익','현금흐름','EPS','BPS','SPS','CFPS','ROE','ROA','부채비율']] 

ps_ts.head(5)

yoy=ps_ts/ps_ts.shift(1)-1    # 전년비 증감률
name=find_ts['Name']
yoy = pd.concat([name,yoy],axis=1).dropna()
print(yoy.head(3))


# 재무비율 순위에 따른 포트폴리오 구성

rebalancing_list = ['2010-04', '2011-04', '2012-04', '2013-04', '2014-04' ,
                    '2015-04', '2016-04','2017-04', '2018-04', '2019-04',   
                    '2020-04', '2021-04', '2022-04','2022-04','2022-04']

fin_list=list(range(2009, 2023))

column_list = ['안정성기준','수익성기준','성장성기준']

portfolio_ret_df = pd.DataFrame(columns=column_list, index = adj_close_ts.loc[rebalancing_list[0]:].index)

for i in range(len(rebalancing_list)):
           
    fin_combi_A =yoy.query('부채비율>0.3').set_index('Name')  
    fin_index_A_list =  fin_combi_A.index
    
    fin_combi_B =yoy.query('매출액>0.3').set_index('Name')  
    fin_index_B_list =  fin_combi_B.index

    fin_combi_C =yoy.query('ROE>0.3').set_index('Name')  
    fin_index_C_list =  fin_combi_C.index
     
    
   ### 포트폴리오 일간수익률
    
    portfolio_ret_df['안정성기준'].loc[rebalancing_list[i]:] = adj_close_ts[fin_index_A_list].loc[rebalancing_list[i]:].pct_change(1).mean(axis=1).dropna()
    portfolio_ret_df['수익성기준'].loc[rebalancing_list[i]:] = adj_close_ts[fin_index_B_list].loc[rebalancing_list[i]:].pct_change(1).mean(axis=1).dropna()
    portfolio_ret_df['성장성기준'].loc[rebalancing_list[i]:] = adj_close_ts[fin_index_C_list].loc[rebalancing_list[i]:].pct_change(1).mean(axis=1).dropna()
   
    # portfolio_ret_df.head(5)
    
    
kindex= adj_close_ts['주가지수']['2010-04-01': ].pct_change(1) # 주가지수 수익률
kindex.iloc[0]=0

portfolio_ret_df.iloc[0] = 0  # 포트폴리오 수익률
portfolio_ret_df = pd.concat([kindex,portfolio_ret_df],axis=1).dropna()

plot_list = ['주가지수','안정성기준','수익성기준','성장성기준']
index_100(portfolio_ret_df[plot_list]).plot()
pp=ret_risk_profile(index_100(portfolio_ret_df[plot_list]))
index_year=index_100(portfolio_ret_df[plot_list]).resample("A").last()
print(pp.round(2))


# %%
