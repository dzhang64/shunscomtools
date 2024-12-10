import pandas as pd
from MyRS.define_func import *
df_data =pd.read_excel('SDR_sdr3_20240705102423.xlsx',sheet_name='RfDevice',skiprows=[1,2,3,4])

df_data.rename(columns={"MOI": "refRfDevice_split", 'description': 'RRU_type'}, inplace=True)
df_data['RRU_type'] = df_data['RRU_type'].apply(lambda z: str_replace(z, ')('))
df_data['RRU_type'] = df_data['RRU_type'].apply(lambda z: str(z).split(',')[0])
df_data['RRU_频段'] = df_data['RRU_type'].apply(lambda xx: xx.split('(')[0])
print(df_data['RRU_type'])