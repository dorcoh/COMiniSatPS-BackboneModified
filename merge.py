import csv
import pandas as pd
import glob

myfiles = glob.glob("*.csv")
df_list = []

for filename in myfiles:
	df = pd.read_csv(filename)
	df.columns = [filename + str(cname) for cname in df.columns]
	df_list.append(df) 

merged = pd.concat(df_list, axis=1)

merged.to_csv('output.csv', header=None, index=None)	