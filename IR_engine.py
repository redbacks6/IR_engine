"""
Python Information Retrieval Engine
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 24 March 2015
"""

### Use cPickle to store and retrieve inverted index.

import nltk, re, os, math, numpy as np
from glob import glob
from pprint import pprint as pp
from nltk.corpus import stopwords

corpus = "/Users/lukejones/Desktop/corpus/this_old_man/doc*.txt"
corpus1 = "/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/blogs/*.txt"
porter = nltk.PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')

def main():
	#clear the console
	os.system('cls' if os.name == 'nt' else 'clear')


	print ('Welcome to the Information Retrieval Engine!')
	print 'The IREngine takes a corpus in the form of directory/documents/*.txt ' \
		  'and lets you query it.'
	keyboard = raw_input("\nEnter the location of your corpus: ")

	index = IREngine(keyboard)

	print ('\nInformation Retrieval Engine is ready!')
	print ('Enter your query or type quit() to quit.')

	while True:
		keyboard = raw_input("\nEnter your query here: ")
		if keyboard.lower() == 'quit()':
			break
		else:
			print('\nTop Results for query: %s' %(keyboard))
			pp(index.query(keyboard)[:10])


"""
This class creates an inverted index in the form of
{Term: IDF, [(DocID, No. Postings)]}

It also has a query function
"""
class IREngine:

	def __init__(self, corpus):

		#corpus = link to a corpus
		self.corpus = corpus
		self.corpus_size = len(glob(corpus))
		# documents = {DocID:|w,d| }
		self.documents = {}
		#inverted_index = {Term: IDF, [(DocID, No. Postings)]}
		self.index = {}

		#build inverted index
		count = 1

		print '\nProcessing Documents. Total Corpus size is %s documents' %(self.corpus_size)
		for document in glob(corpus):
			raw = open(document).read()
			doc = [os.path.basename(document),process_text_doc(raw)]
			self.documents[doc[0]] = {}
			self.documents[doc[0]] = len(doc[1])
			self.index = add_doc_to_index(doc, self.index)
			
			if (count % 500) == 0:
				print "Processed %s of %s documents" %(count, self.corpus_size)
			
			# if count > 1000:
			# 	break
			count += 1

		#finalise inverted index
		updateIDF(self.index,self.documents)


	"""
	Query Index
	Input: Query as a string
		   Inverted Index as {'token': (IDF, {'document': no. postings}}
	Method: Sum the results of TF x IDF for each document
			Normalise by dividing by the length of the document
	Output: Ranked results
	Return: [document, score]
	"""

	def query(self, terms):

		query = process_text_doc(terms)

		results = {}
		for key in self.documents:
			results[key] = 0

		for term in query:
			if term in self.index:
				for document in self.index[term][1]:
					results[document] = results[document] + self.index[term][1][document] * self.index[term][0]

		finalresults = []

		for document in results:
			if results[document] != 0 and self.documents[document] != 0:
				finalresults.append((document, results[document]/(self.documents[document])))

		if finalresults:	
			return sorted(finalresults, key=lambda result:result[1], reverse=True)
		else:
			return ['There seems to be no results for your query']


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
