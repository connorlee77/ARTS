import numpy as np 
import matplotlib
import pandas as pd 
import os 
import matplotlib.pyplot as plt
import sklearn
from pandas.stats.api import ols


def getDataFrame(path, filename):
    os.chdir(path)
    frame = pd.DataFrame.from_csv(filename, index_col=False, infer_datetime_format=True)
    return frame


if __name__ == "__main__":
	PATH = '../data/mergedData/'
	df = getDataFrame(PATH, "For_Jim.csv")
	res = ols(y=df['Avg Arrival Diff'], x=df[['Date','20cc','51','52','60','32','31','20cw','10','40']], intercept = True)
	print(res)
