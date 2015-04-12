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
	MAP: returns mean average precision for a given query
	Print P-R Curve: Prints the P-R curve for a given query
    Precision@k: Returns the precision at k
"""
class queryevaluation:

    def __init__(self, results, qrels, query):
        self.querytext = query[1]
        self.querynumber = query[0]
        self.results = results
        self.qrels = process_qrels(qrels)
        self.vector = results_vector(self.results[self.querynumber], self.qrels[self.querynumber])
        self.pr_array = pr_array(self.vector, self.qrels[self.querynumber])

    """
	Mean Average Precision
    Returns: Mean average precision for a given query
	"""
    def MAP(self, query_no):

		MAP = 0.0
		for k in range(len(self.vector)):
		    MAP += self.vector[k] * prec_at_k(self.vector, k+1)

		return MAP / len(self.qrels[query_no])

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
        plt.title("Query %s: "%(self.querynumber)+self.querytext)
        plt.show()

        pass

    """
	Return Precision at K
	"""
    def return_pratk(self, k):
        return prec_at_k(self.vector, k)


"""
Creates a results vector
Input: ranked results {docID: rank_score}, qrels{docID: relevance}
Output: binary results vector for each document []
"""
def results_vector(results, qrels):
	results_vector = []

	rankedresults = [[docID, results[docID]] for docID in sorted(results, key = results.get, reverse = True)]

	for result in rankedresults:
		if result[0] in qrels:
			results_vector.append(1)
		else:
			results_vector.append(0)

	return results_vector


"""
processed qrels
input: space deliminated text file in form of: <query number> <number> <documentID> <relevance>
outputs: 
	QRels: {query number: {docID: relevance}}
	Relcount: int (number of relevant documents)

"""
def process_qrels(file_ext):

	qrels = {}

	with open(file_ext, 'r') as qfile:
		for line in qfile:
			qrel = line.split()

			query_number = int(qrel[0])
			docID = qrel[2]
			relevance = int(qrel[3])

			if query_number not in qrels and relevance > 0:
				qrels[query_number] = {docID: relevance}
			elif relevance > 0:
				qrels[query_number][docID] = relevance

	return qrels


"""
Precision at K
"""
def prec_at_k(vector, k):
    if k > len(vector):
        if len(vector) > 0:
            k = len(vector)
        else: return 0

    # set length of vector based on results
    k_vector = vector[:k]

    return precision(k_vector)


"""
Precision Recall Array
Use to produce a PR Curve
"""
def pr_array(vector, qrels):

    pr_array = []

    for index, item in enumerate(vector):
        point = [
            recall(vector[:index + 1], qrels), precision(vector[:index + 1])]
        pr_array.append(point)

    return pr_array


"""
Precision
"""
def precision(vector):
    # add the length of the vector
    prec = 0.0
    for result in vector:
        prec += result
    prec = prec / len(vector)

    return prec


"""
Recall
"""
def recall(vector, qrels):
    recall = 0.0
    for result in vector:
        recall += result
    recall = recall / len(qrels)

    return recall


# Run the Main Method
if __name__ == '__main__':
    main()
