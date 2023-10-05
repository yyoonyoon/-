#%%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import os
from dateutil.relativedelta import relativedelta

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
DATA_FILE = "KRX300_FIN_DATA_2023.xlsx"

# pd.ExcelFile() 함수를 사용하여 엑셀 파일을 열기
data_wb = pd.ExcelFile(folder_dir + "/" + DATA_FILE)

# find_ts라는 새로운 데이터프레임에 재무시트를 읽어와서 저장
find_ts = data_wb.parse("재무", index_col=3)  # 인덱스는 연도

#자기자본 정의
find_ts['자기자본'] = find_ts['총자본'] - find_ts['총부채']

#ROE 정의
find_ts['ROE'] = (find_ts['당기순이익'] / find_ts['자기자본']) * 100
#--------------------------------------------------------------


# 전년 대비 영업이익 증가율 (상위 10종목)
find_ts['영업이익 증가율'] = (find_ts['영업이익'] - find_ts['영업이익'].shift(1)) / find_ts['영업이익'].shift(1) *100
top_10_profit_growth = find_ts[(find_ts.index == 2022)].nlargest(10, '영업이익 증가율')
#결과출력
# print(top_10_profit_growth)
# 그래프 그리기
# plt.figure(figsize=(10, 6))
# plt.bar(find_ts['회계연도'], find_ts['영업이익 증가율'])
# plt.xlabel('날짜')
# plt.ylabel('영업이익 증가율 (%)')
# plt.title('2022년 영업이익 증가율 상위 10개 종목')
# plt.xticks(rotation=45)
# plt.tight_layout()




# 2022년 기준 3개년 평균 ROE 계산
find_ts['avg_ROE'] = (find_ts['ROE'] + find_ts['ROE'].shift(1) + find_ts['ROE'].shift(2)) / 3
# 2022년 기준 평균 ROE가 20% 이상인 기업 선택 (상위 10개)
top_10_roe = find_ts[find_ts.index == 2022].nlargest(10, 'avg_ROE')
# 결과 출력
# print(top_10_roe[['Name', 'avg_ROE']])


# 2022년 기준 주당 현금흐름(CFPS) 증가율 계산
find_ts['CFPS_Growth'] = (find_ts['CFPS'] - find_ts['CFPS'].shift(1)) / find_ts['CFPS'].shift(1) * 100
# 2022년 기준 주당 현금흐름(CFPS) 증가율 상위 10종목 선택
top_10_cfps_growth = find_ts[find_ts.index == 2022].nlargest(10, 'CFPS_Growth')
# 결과 출력
# print(top_10_cfps_growth[['Name', 'CFPS_Growth']])



# 2022년 기준 매출액 증가율 계산
find_ts['매출액 증가율'] = (find_ts['매출액'] - find_ts['매출액'].shift(1)) / find_ts['매출액'].shift(1) * 100
over_30 = find_ts[(find_ts.index == 2022) & (find_ts['매출액 증가율'] >= 30)].nlargest(10, '매출액 증가율')
# 2022년 기준 영업 이익 증가율 계산
find_ts['영업 이익 증가율'] = (find_ts['영업이익'] - find_ts['영업이익'].shift(1)) / find_ts['영업이익'].shift(1) * 100
over_20 = find_ts[(find_ts.index == 2022) & (find_ts['영업 이익 증가율'] >= 20)].nlargest(10, '영업 이익 증가율')
# 매출액 증가율 30% 이상 & 영업 이익 증가율 20% 이상 (매출액 기준 상위 10종목 중) 교집합 구하기
merged = pd.merge(over_20, over_30)
# print(merged[['Name', '매출액 증가율', '영업 이익 증가율']])


# 매출액 순이익률 30% 이상 기업 (상위 10위)
find_ts['순이익률'] = find_ts['당기순이익'] / find_ts['매출액'] * 100
top_10_net_profit_margin = find_ts[(find_ts.index == 2022) & (find_ts['순이익률'] >= 0.3)].nlargest(10, '순이익률')
print(top_10_net_profit_margin[['Name', '순이익률']])

find_ts['부채비율'] = find_ts['총부채'] / find_ts['총자본'] * 100
top_10_net_profit_margin = find_ts[(find_ts.index == 2022)].nlargest(10, '부채비율')
print(top_10_net_profit_margin[['Name', '부채비율']])



# # 조건을 만족하는 종목 출력
# print("전년 대비 영업이익 증가율 (상위 10종목):")
# print(top_profit_growth)
# top_profit_growth.plot()

# print("\n3개년 평균 ROE 20% 이상 기업 (상위 10위):")
# print(top_roe_3yr_avg)

# print("\n주당 현금흐름(CFPS) 증가율 (상위 10종목):")
# print(top_cfps_growth)

# print("\n매출액 증가율 30% 이상 & 영업 이익 증가율 20% 이상 (매출액 기준 상위 10종목):")
# print(top_revenue_profit_growth)

# print("\n매출액 순이익률 30% 이상 기업 (상위 10위):")
# print(top_net_profit_margin)
# %%



####매출액 증가율 30% 이상 & 영업 이익 증가율 20% 이상 (매출액 기준 상위 10종목) 이부분 부터 하기.
#두개의 데이터프레임 열에 있는 원소들을 비교해서 새로만든 열에 넣어서 교집합을 뽑아 내야 할 듯
#find_ts['FFF'] = (find_ts['매출액 증가율'] >= 30) & (find_ts['영업 이익 증가율'] >= 20) 이런 방식으로는 두 컬럼이 충돌해서 불가