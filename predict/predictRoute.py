import pandas as pd 
import numpy as np 
from datetime import datetime
from sklearn import preprocessing

DATA = 'output/stations.csv'


def isWeekday(dt):
	return 1 if dt.weekday() < 5 else 0

def getSeconds(dt):
	seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
	return seconds

def toDatetime(timestamp):
	return datetime.strptime(timestamp['Date'], '%Y-%m-%d %H:%M:%S')


class Arm:

	def __init__(self, route, num_features):
		self.name = route 
		self.A = np.identity(num_features)
		self.b = np.zeros(num_features)


class PredictRouteOnline:

	def __init__(self):

		self.results_maxmin = 0
		self.results_mean = 0
		self.frame = None
		self.true_labels = None

		# Fill in state variables
		self.importData()
		self.prepData()

		# Initialize arms
		self.arm_names = self.true_labels.unique()
		self.arms = {}
		self.num_features = len(self.frame.columns)
		self.initArms(self.arm_names, self.num_features)

		# Regret
		self.expected_payoff = 0
		self.true_payoff = 0
		self.regret = 0


	def importData(self):
		self.frame = pd.DataFrame.from_csv(DATA, index_col=False, infer_datetime_format=True)
		return self.frame

	def prepData(self):
		label_encoder = preprocessing.LabelEncoder()

		result = pd.get_dummies(self.frame, columns=['FareProduct', 'TransactionType'], dummy_na=True)	

		result['weekday'] = None
		result['time'] = None

		for index, row in result.iterrows():

			dt = toDatetime(row)
			seconds = getSeconds(dt)
			weekday = isWeekday(dt)

			result.set_value(index, 'time', seconds)
			result.set_value(index, 'weekday', weekday)

		self.true_labels = result['Route']

		result.drop(['Departure', 'Arrival', 'Hour', 'Minute', 'Date', 'Route', 'station'],inplace=True,axis=1)

		self.results_mean = result.mean()
		self.results_maxmin = result.max() - result.min() 

		result_norm = (result - self.results_mean) / self.results_maxmin
		result_norm.fillna(value=0, inplace=True)

		self.frame = result_norm
		return result_norm


	def initArms(self, arms, num_features):

		arms_objs = {}
		for arm in arms:
			arms_objs[arm] = Arm(arm, num_features)

		self.arms = arms_objs
		return self.arms


	def LinUCB(self, learning_rate=0.01, payoff=1.0, loss=0):

		for index, row in self.frame.iterrows():

			features = row.as_matrix()
			assert len(features) == self.num_features
			
			probabilities = np.zeros(len(self.arm_names))
			for i, a in enumerate(self.arm_names):
				
				if a not in self.arms:
					self.arms[a] = Arm(a, self.num_features)


				curr_arm = self.arms[a]
		
				A = curr_arm.A 
				b = curr_arm.b

				A_inv = np.linalg.inv(A)
				xTAx = np.dot(
					np.dot(
						features.T, 
						A_inv), 
					features)

				theta = np.dot(A.T, b)
				p = np.dot(theta.T, features) + learning_rate * np.sqrt(xTAx)  

				probabilities[i] = p

			maxIndex = np.argmax(probabilities)
			chosenArm = self.arm_names[maxIndex]
			arm = self.arms[chosenArm]

			trueLabel = self.true_labels.get_value(index, 'Route')

			# Calculate reward and regret
			reward = payoff if trueLabel is chosenArm else loss

			self.expected_payoff += reward
			self.true_payoff += payoff
			self.regret = self.true_payoff - self.expected_payoff

			# Update arm feature weights 
			arm.A = np.add(arm.A, 
				np.dot(features, features.T))

			arm.b = np.add(arm.b, 
				np.dot(reward, features))
			
			if (index + 1) % 100 == 0:
				print str(index) + ', regret: ' + str(self.regret)




def main():
	learner = PredictRouteOnline()
	learner.LinUCB()

if __name__ == '__main__':
	main()