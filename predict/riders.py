import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

path = './output/stations.csv'
products = ['Reg SV College', 'PS CTW', 'EZ Pass S/D Z2', 'EZ Pass S/D Z3', 'EZ Pass S/D Z0', 'EZ Pass S/D Z1', 'PS Try Tran Mon', 'DCFS EZ (New)', 'EZ PassS/D Repl', 'Reg SV Student', 'EZ Annual Z0', 'EZ Annual Z1', 'EZ Annual Z5', 'Reg Senior 60', 'EZ Pass AdultZ1', 'EZ Pass AdultZ0', 'EZ Pass AdultZ2', 'ASI', 'EZ Pass AD Repl', 'Reg SV Sr/Dis', 'Reg SV Regular']


def importTAPData():
	frame = pd.DataFrame.from_csv(path, index_col=False, infer_datetime_format=True)
	return frame 

def graph():

	frame = importTAPData()

	titles = []
	graphs = []
	for prod in ['ASI', 'Reg SV Regular', 'Reg SV Sr/Dis']:

		if prod == 'Unnamed: 0':
			continue
		else:
			f = frame[frame['FareProduct'] == prod].groupby('station').size()
			print f
			graphs.append(f)
			titles.append(prod)

	for i, graph in enumerate(graphs):
		fig = plt.gcf()
		graph.plot(x='Station', y='Transactions (4/11 - 4/30)', kind='bar', title='Count of ' + titles[i] + ' at Different Stations from 4/11 - 4/30')
		plt.xlabel('Stations')
		plt.ylabel('Count')
		fig.subplots_adjust(bottom=0.55)
		plt.savefig('output/' + 'stations' + str(i) + ".png")
		plt.clf()


def countProd():

	frame = importTAPData()
	f=frame.groupby('FareProduct').size()
	f.plot(title='Count of Different Fare Products used from 4/11-4/30', kind='bar')
	plt.xlabel('Fare Product')
	plt.ylabel('Count')
	plt.gcf().subplots_adjust(bottom=0.30)

	plt.savefig('output/' +"countFareProduct.png")
	plt.clf()

countProd()
graph()