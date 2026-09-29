import pandas as pd

df=pd.read_csv("test_results.csv")
print(df.columns)
print("Length of dataframe : ",len(df))

w=df[df["undertone"]=='Warm']
c=df[df["undertone"]=='Cool']
n=df[df["undertone"]=='Neutral']

print("Total no of warm : ", len(w))
print("Total no of cool : ", len(c))
print("Total no of neutral : ", len(n))

l=df[df["complexion"]=='Light']
m=df[df["complexion"]=='Medium']
d=df[df["complexion"]=='Dark']

print("Total no of light : ", len(l))
print("Total no of medium : ", len(m))
print("Total no of dark : ", len(d))