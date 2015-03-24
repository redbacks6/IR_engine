"""
Python script to tokenise a document 
Author: Luke Jones
Email: lukealexanderjones@gmail.com
Student ID: 654645
Date: 14 March 2015
"""

import nltk, re, os, math, numpy as np
from glob import glob
from pprint import pprint as pp
from nltk.corpus import stopwords

corpus = "/Users/lukejones/Desktop/corpus/this_old_man/doc*.txt"
corpus1 = "/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/blogs/*.txt"


porter = nltk.PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')

def main():

	index = {}
	documents = {}

	count = 1

	for document in glob(corpus):
		raw = open(document).read()
		doc = [os.path.basename(document),process_text_doc(raw)]
		documents[doc[0]] = {}
		documents[doc[0]] = len(doc[1])
		index = add_doc_to_index(doc, index)
		print "Added %s to index. Total processed docs = %s" %(doc[0], count)
		
		# if count > 1000:
		# 	break

		count += 1

	updateIDF(index,documents)

	queryresults = query_index('old man',index, documents)

	print ('\nQuery Results')
	pp(queryresults[:10])


def updateIDF(index, documents):
	N = float(len(documents))

	for term in index:
		dft = len(index[term][1])
		index[term][0] += math.log(N/dft)

	pass

"""
Create an inverted index
Input: Document [filename, [tokens]]
       Inverted Index {} or {'token': (IDF, {'document': no. postings}}
Output: Inverted Index
Return: {'token': (IDF, {'document': no. postings}}
"""
def add_doc_to_index(document, index):
	
	for token in document[1]:

		IDF = 0 #placeholder

		if token not in index:
			index[token] = [IDF,{document[0]:1}]
		elif document[0] not in index[token][1]:
			index[token][1][document[0]] = 1
		else:
			index[token][1][document[0]] += 1

	return index

"""
Query Index
Input: Query as a string
	   Inverted Index as {'token': (IDF, {'document': no. postings}}
Method: Sum the results of TF x IDF for each document
		Normalise by dividing by the length of the document
Output: Ranked results
Return: TBC
"""
def query_index(string_query, index, documents):
	query = process_text_doc(string_query)

	results = {}
	for key in documents:
		results[key] = 0

	for term in query:
		for document in index[term][1]:
			results[document] = results[document] + index[term][1][document] * index[term][0]

	finalresults = []

	for document in results:
		if results[document] != 0 and documents[document] != 0:
			finalresults.append((document, results[document]/(documents[document])))

	return sorted(finalresults, key=lambda result:result[1], reverse=True)


"""
Processes a text document (no HTML) into tokens
Input: document as a string
Output: Tokenised document
Return: [filename, [tokens]]
"""

def process_text_doc(document):
	#remove formatting and punctuation and non alpha numeric characters
	#fold to lower case
	cleaned = re.sub(r'[^a-z1-9 ]+', ' ', document.lower())
	#tokenise and stem (using the Porter stemmer)
	stemmed_tokens = [porter.stem(t) for t in nltk.word_tokenize(cleaned)]
	#remove stopwords
	final_list = [w for w in stemmed_tokens if w not in stopwords]

	return final_list



# Run the Main Method
if __name__ == '__main__':
    main()