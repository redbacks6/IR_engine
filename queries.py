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
corpus = "/Users/lukejones/Desktop/corpus/this_old_man/doc*.txt"
qrels = '/Users/lukejones/Desktop/corpus/qrels.this_old_man.txt'

#Assignment corpus
corpus1 = "/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/blogs/*.txt"
qrels1 = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/06.topics.851-900.txt'

#Save and load index
output_index = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1index/index1.pkl'
output_documents = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1index/documents1.pkl'

def main():

	querynumber = 851
	index = invertedindex()
	index.build_index(corpus)
	# # index.write_index_to_file(output_index, output_documents)
	# # index.load_index(output_index, output_documents)
	results = {querynumber: index.query('old man')}

	evalu = queryevaluation(results, qrels, querynumber)

	print evalu.MAP()

	evalu.print_prcurve()

"""
Extract querys from the text file and add to query_array
"""
def extract_queries():
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
