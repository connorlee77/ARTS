import csv
import pandas as pd 


def importTimetable(file):
	return pd.DataFrame.from_csv(file, index_col=False, infer_datetime_format=True) 

def main():
	dt = importTimetable('stations.csv')
	print dt
if __name__ == '__main__':
	main()