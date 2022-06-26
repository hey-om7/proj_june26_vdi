import pandas as pd
import re

df = pd.read_csv("file.csv")
pd.set_option('display.max_colwidth', 199)

rawRegex = r"(\ - Import ended at )|(\ Import duration )"
df['message'].str.split(rawRegex, expand=True)

df['date'] = df['message'].str.extract(r"([0-9]{4}-[0-9]{2}-[0-9]{2})")

df['end_time'] = df['message'].str.extract(
    r"([0-9]{2}:[0-9]{2}:[0-9]{2}((\ PM)|(\ AM)|(\ -)))")[0]


def makeCorrection(x):
    if"PM" in x:
        return(str(int(x.split(":")[0])+12)+x[2:-3]).strip()
    else:
        if("AM" in x):
            return x[:-3]
        return x[:-2]


df['end_time'] = df['end_time'].apply(lambda x: makeCorrection(x))

df['duration'] = df['message'].str.extract(
    r"((?<=duration\ )[0-9]{2}\:[0-9]{2}\:[0-9]{2}([\.0-9]+)*)")[0]

df['Type'] = df['message'].str.extract(r"([A-Za-z\ ]+(?=\ \-))")

df = df.drop("message", axis='columns')

s1 = df['end_time'].str.split(":", expand=True)
s2 = df['duration'].str.split(":", expand=True)
s3 = pd.DataFrame()

s3['hours'] = s1[0].astype(int)-s2[0].astype(int)
s3['mins'] = s1[1].astype(int)-s2[1].astype(int)

s3['seconds'] = s1[2].astype(float)-s2[2].astype(float)
s3['seconds'] = s3['seconds'].apply(lambda x: round(x))
s3['startTime'] = s3['hours'].astype(
    str)+":"+s3['mins'].astype(str)+":"+s3['seconds'].astype(str)

df["start_time"] = s3['startTime']
df["duration"] = df["duration"].apply(
    lambda x: (x.split(".")[0]) if "." in x else x)
print(df)
