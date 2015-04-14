"""
Python Implementation of a 'bag of words' inverted index.

Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 27 March 2015
"""

"""
TODO
1)
2)
"""

import nltk, re, os, math
from glob import glob
from pprint import pprint as pp
from nltk.corpus import stopwords
try:
    import cPickle as pickle
except:
    import pickle

porter = nltk.PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')

def main():
	
	# run_as_program()

	pass

"""
This class creates an inverted index in the form of
index = {'token': [IDF, {'documentID': [posting1, posting2, posting_i]}]}
document = {‘DocID’:|w,d|}

It also has a query function
"""
class invertedindex:

	def __init__(self):
		#corpus = link to a corpus
		self.corpus = ''
		# documents = {DocID:|w,d| }
		self.documents = {}
		#inverted_index = {Term: IDF, [(DocID, No. Postings)]}
		self.index = {}

	"""
	Builds an inverted index from a corpus
	"""
	def build_index(self, corpus):
		self.corpus = corpus
		process_corpus(self.corpus, self.index, self.documents)

	def load_index(self, index, documents):
		index_file = open(index, 'rb')
		docs_file = open(documents, 'rb')

		self.index = pickle.load(index_file)
		self.documents = pickle.load(docs_file)	


	"""
	Query Index
	Input: Query as a string
	Method: Sum the results of TF x IDF for each document
			Normalise by dividing by the length of the document
	Output: Ranked results
	Return: {documentID, score}
	"""
	def query(self, terms):
		query = process_text_doc(terms)
		results = {}
		finalresults = {}

		for key in self.documents:
			results[key] = 0

		for term in query:
			if term in self.index:
				for document in self.index[term][1]:
					results[document] = results[document] + self.index[term][1][document] * self.index[term][0]

		for document in results:
			if results[document] != 0 and self.documents[document] != 0:
				finalresults[document] = results[document]/self.documents[document]

		if finalresults:	
			return finalresults
		else:
			return ['There seems to be no results for your query']


	"""
	Writes the index to a file for quick retrieval later
	Input: URL of file
	"""
	def write_index_to_file(self, index_url, documents_url):
		index_doc = open(index_url,"wb")
		docs_doc = open(documents_url,"wb")

		index_string = pickle.dump(self.index, index_doc, -1)
		documents_string = pickle.dump(self.documents, docs_doc, -1)

		index_doc.close()
		docs_doc.close()


"""
Processes corpus and updates an index and documents dictionary
Input: link to corpus in the form of "/directory/subdirectory/*.txt"
Output: Inverted index and documents list
"""
def process_corpus(corpus, index, documents):
	#build inverted index
	count = 1
	corpus_size = len(glob(corpus))

	print '\nProcessing Documents. Total Corpus size is %s documents' %(corpus_size)
	
	filename = re.compile(ur'^(.*)\/(.*)(\..*)$')

	for document in glob(corpus):
		name = re.search(filename, document)
		docID = name.group(2)

		raw = open(document).read()
		processed_doc = process_text_doc(raw)

		doc = [docID , processed_doc]
		documents[doc[0]] = document_normalisation(processed_doc)
		index = add_doc_to_index(doc, index)
		
		if (count % 500) == 0:
			print "Processed %s of %s documents" %(count, corpus_size)
		
		# if count > 1000:
		# 	break
		count += 1

	#finalise inverted index
	updateIDF(index, documents)		

	return index, documents		

def updateIDF(index, documents):
	N = float(len(documents))

	for term in index:
		dft = len(index[term][1])
		index[term][0] += math.log(N/dft)

	pass

"""
Returns a document length normalisation factor
"""
def document_normalisation(processed_doc):
	
	document_terms = {}
	normalisation_factor = 0.0

	for term in processed_doc:
		if term in document_terms:
			document_terms[term] += 1.0
		else: document_terms[term] = 1.0

	total_terms = len(document_terms)

	for term in document_terms:
		normalisation_factor += document_terms[term]/total_terms

	return math.sqrt(normalisation_factor)

		

"""
Adds a document to the inverted index
Input: Document [filename, [tokens]]
       Inverted Index {} or {'token': [IDF, {'document': no. postings}]}
Output: Inverted Index
Return: {'token': [IDF, {'document': no. postings}]}
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
