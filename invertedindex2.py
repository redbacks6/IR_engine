"""
Python implementation of an inverted index with positional
indices.

Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 12 April 2015
"""

"""
TODO
1) 

"""

import nltk, re, os, math, time
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
{'token': [IDF, {'documentID': [posting1, posting2]}]}

Note: posting indices stored as offsets from previous

It also has a query function (refer below)
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
		print "Loading index..."
		t0 = time.time()

		index_file = open(index, 'rb')
		docs_file = open(documents, 'rb')

		self.index = pickle.load(index_file)
		self.documents = pickle.load(docs_file)	

		t1 = time.time()
		print "Loading completed in {} seconds".format(t1-t0)


	def print_index(self):
		print pp(self.documents)
		print pp(self.index)


	"""
	Query Index
	Input: Query as a string
		   Inverted Index as {'token': [IDF, {'documentID': [posting1, posting2]}]}
	Method: Sum the results of TF x IDF for each document
			Normalise by dividing by the length of the document
	Output: Ranked results
	Return: {documentID: score}
	"""
	def query(self, terms):
		#indices for Document input
		DocID = 0
		token_list = 1
		#indices for Inverted index input
		IDF = 0
		DocPostings = 1

		phrase_check = re.compile(ur'[\'|"].+[\'|"]')
		phrasequery = re.search(phrase_check, terms)

		if phrasequery:
			query = process_text_doc(terms)
			results = {}
			phrase_docs = {}

			#create a list of documents matching the first query term
			for document in self.index[query[0]][DocPostings]:
				results[document] = 1

				#cycle through the terms in the query and ammend the documents
				#list with a 1 if the terms are in the correct order or
				#zero if in the incorrect order
				for i, term in enumerate(query):
					for posting in self.index[query[0]][DocPostings][document]:
						posting_qi = posting + i

						try:
							if posting_qi in self.index[term][DocPostings][document]:
								results[document] *= 1
								break

							else: 
								results[document] *= 0
								break

						except KeyError:
							results[document] *= 0
							break 

			# Created a reduced document list with only the documents
			# matching the phrase query.
			for document in results:
				if results[document] > 0:
					phrase_docs[document] = self.documents[document]

			ranked_documents = ranked_results(self.index, phrase_docs, terms, True)
			
			#last check to see if phrase query improved results.
			#If no results, then just use bag of words results
			if len(ranked_documents) > 0:
				return ranked_documents
			else: return ranked_results(self.index, self.documents, terms, False)	

		else:
			return ranked_results(self.index, self.documents, terms, False)


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
Return ranked results for a query
"""
def ranked_results(index, documents, terms, positional):
	#indices for Document input
	DocID = 0
	token_list = 1
	#indices for Inverted index input
	IDF = 0
	DocPostings = 1

	query = process_text_doc(terms)
	results = {}
	finalresults = {}

	for document in documents:
		results[document] = 0

	for term in query:
		if term in index:
			if positional:
				for document in results:
					results[document] = results[document] + len(index[term][DocPostings][document]) * index[term][IDF]

			else:
				for document in index[term][DocPostings]:
					results[document] = results[document] + len(index[term][DocPostings][document]) * index[term][IDF]

	for document in results:
		if results[document] != 0 and documents[document] != 0:
			finalresults[document] = results[document]/documents[document]

	if finalresults:	
		return finalresults
	else:
		return {}


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

"""
Modifies the IDF to reflect the documents in index
"""
def updateIDF(index, documents):
	#indices for Inverted index input
	IDF = 0
	DocPostings = 1

	N = float(len(documents))

	for term in index:
		dtf = len(index[term][DocPostings])
		index[term][IDF] += math.log(N/dtf)

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
Input: Document [DocID, [tokens]]
       Inverted Index {} or {'token': [IDF, {'DocID': [posting1, posting2]}]}
Output: Inverted Index
Return: {'token': [IDF, {'DocID': [posting1, posting2]}]}
"""
def add_doc_to_index(document, index):
	#indices for Document input
	DocID = 0
	token_list = 1

	#indices for Inverted index input
	IDF = 0
	DocPostings = 1

	for i, token in enumerate(document[token_list]):

		IDF = 0 #placeholder

		if token not in index:
			index[token] = [IDF,{document[DocID]:[i]}]
		elif document[DocID] not in index[token][DocPostings]:
			index[token][DocPostings][document[DocID]] = [i]
		else:
			index[token][DocPostings][document[DocID]].append(i)

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
