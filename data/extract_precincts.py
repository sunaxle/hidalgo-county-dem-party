import pandas as pd

df = pd.read_excel('temp_districts/PLANC2333_r110_VTD24G.xls', header=None)
for i in range(30):
    print(i, df.iloc[i].dropna().tolist())
