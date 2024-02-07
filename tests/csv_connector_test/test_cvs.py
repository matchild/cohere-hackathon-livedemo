import pandas as pd

a = pd.read_csv("biostats.csv")
print(a.select_dtypes(include=["category", "object"]))
