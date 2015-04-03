"""
Evaluation Package
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 28 March 2015
"""
from pprint import pprint as pp
from invertedindex import invertedindex
import matplotlib.pyplot as plt

def main():

	pass

"""
Query evaluation object
Inputs:
	Ranked results: {querynumber: {documentID: rank_score}}
	Query relevance: space deliminated text file in form of: <query number> <number> <documentID> <relevance>
	Total relevant results: int (number of relevant documents)
	Query number: int (reference number of the query)

Methods: 
	MAP: returns mean average precision of a query
	Print P-R Curve: Prints the P-R curve of a query	
"""

class queryevaluation:

	def __init__(self, results, qrels, querynumber):

		self.results = results
		self.qrels, self.totalrelevant = process_qrels(qrels)
		self.vector = results_vector(results[querynumber], self.qrels[querynumber])
		self.pr_array = pr_array(self.vector, self.qrels[querynumber])

	
	"""
	Mean Average Precision
	"""
	def MAP(self):

		MAP = 0.0
		for k in range(len(self.vector)):
			MAP += self.vector[k] * prec_at_k(self.vector,k+1)
			if k == 1000: break
		
		MAP = MAP/self.totalrelevant

		return MAP

	"""
	Print P-R Curve
	"""
	def print_prcurve(self):
		precision = []
		recall = []

		for i in self.pr_array:
			precision.append(i[0])
			recall.append(i[1])

		plt.plot(precision, recall)
		plt.ylabel("Precision")
		plt.xlabel("Recall")
		plt.show()

		pass


"""
Creates a results vector
Input: ranked results {docID: rank_score}, qrels{docID: relevance}
Output: binary results vector for each document []
"""
def results_vector(results, qrels):
	vector = []
	finalvector = []

	for doc in results:
		vector.append([doc, results[doc]])

	vector = sorted(vector, key = lambda vector: vector[1], reverse=True)

	for result in vector:
		if result[0] in qrels:
			if qrels[result[0]] >= 1:
				finalvector.append(1)
			else:
				finalvector.append(0)
		else: finalvector.append(0)

	return finalvector


"""
processed qrels
input: space deliminated text file in form of: <query number> <number> <documentID> <relevance>
outputs: 
	QRels: {query number: {docID: relevance}}
	Relcount: int (number of relevant documents)

"""
def process_qrels(file_ext):

	qrels = {}
	relcount = 0

	with open(file_ext, 'r') as qfile:
		for line in qfile:
			qrel = line.split()

			query_number = int(qrel[0])
			docID = qrel[2]
			relevance = qrel[3]

			if relevance >= 1:
				relcount += 1

			if query_number not in qrels:
				qrels[query_number] = {docID: relevance}
			else:
				qrels[query_number][docID] = relevance

	return qrels, relcount


"""
Precision at K
"""
def prec_at_k(vector, k):
	if k > len(vector):
		return "k greater than results returned"
	
	#set length of vector based on results	
	k_vector = vector[:k]

	return precision(k_vector)


"""
Precision Recall Array
Use to produce a PR Curve
"""
def pr_array(vector, qrels):

	pr_array = []

	for index, item in enumerate(vector):
		point = [recall(vector[:index+1], qrels),precision(vector[:index+1])]
		pr_array.append(point)

	return pr_array


"""
Precision
"""
def	precision(vector):
	#add the length of the vector
	prec = 0.0
	for result in vector:
		prec += result
	prec = prec/len(vector)

	return prec


"""
Recall
"""
def recall(vector,qrels):
	recall = 0.0
	for result in vector:
		recall += result
	recall = recall/len(qrels)

	return recall


# Run the Main Method
if __name__ == '__main__':
    main()	