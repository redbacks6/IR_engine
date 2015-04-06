"""
Query Processor
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 24 March 2015
"""

import re 
from pprint import pprint as pp
from invertedindex import invertedindex
from queryevaluation import queryevaluation

#Test corpus
corpus = '/Users/lukejones/Desktop/corpus/this_old_man/doc*.txt'
qrels = '/Users/lukejones/Desktop/corpus/qrels.this_old_man.txt'

#Assignment corpus
corpus1 = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/blogs/*.txt'
queryfile = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/06.topics.851-900.txt'
qrels1 = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/qrels.february.txt'

#Save and load index
output_index = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1index/index1.pkl'
output_documents = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1index/documents1.pkl'

def main():

	queries = extract_queries(queryfile)

	index = invertedindex()
	# index.build_index(corpus1)
	# index.write_index_to_file(output_index, output_documents)
	index.load_index(output_index, output_documents)

	MAParray = []
	
	# map_array(index, queries, MAParray)

	query = queries[20]
	results = {query[0]: index.query(query[1])}
	evalu = queryevaluation(results, qrels1, query[0])

	evalu.print_prcurve()


	pass



def map_array(index, queries, maparray):	

	for query in queries:

		results = {query[0]: index.query(query[1])}
		evalu = queryevaluation(results, qrels1, query[0])
		MAParray.append([query[0],evalu.MAP()])

	print pp(MAParray)

	return MAParray


"""
Extract querys from the text file and add to query_array
Input: file address
Output: [[int(topicnumber), str(query)]]
"""
def extract_queries(url):
	query_text = open(url).read()
	title = re.compile(r"(?<=<title>\s).*")

	#starting number of the topic
	topic = 851
	query_array = []

	output = title.findall(query_text)

	for query in output:	
		query_array.append((topic,query))
		topic += 1

	return query_array


# Run the Main Method
if __name__ == '__main__':
    main()	
