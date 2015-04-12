"""
Query Processor
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 24 March 2015
"""

import re
import csv
from pprint import pprint as pp
from invertedindex2 import invertedindex
from queryevaluation import queryevaluation
from nltk.corpus import stopwords

# Test corpus
corpus = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/test_corpus/this_old_man/doc*.txt'
qrels = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/test_corpus/qrels.this_old_man.txt'

# Assignment corpus
corpus1 = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/blogs/*.txt'
queryfile = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/06.topics.851-900.txt'
qrels1 = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/qrels.february.txt'

# Save and load index
output_index = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1index/index2.pkl'
output_documents = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1index/documents2.pkl'

# Outputfile
output_file = '/Users/lukejones/Desktop/Evaluation_Metrics2.csv'

k_value = 10


def main():

    queries = extract_queries(queryfile)

    index = invertedindex()
    # index.build_index(corpus1)

    # index.write_index_to_file(output_index, output_documents)
    index.load_index(output_index, output_documents)

    # print pp([[docID, index.query(query)[docID]] for docID in sorted(index.query(query), key = index.query(query).get, reverse = True)])

    write_results(index, queries, output_file)

    # pr_curve(index, queries, 880)

    pass

"""
Inputs: 
Outputs: csv file with evaluation metrics
"""
def write_results(index, queries, outputfile):

    with open(outputfile, 'w') as outputcsv:
        writer = csv.DictWriter(
            outputcsv, ['query_no', 'query_text', 'prec@10', 'mean_average_precision'])

        writer.writeheader()

        for query in queries:

            data = {}

            results = {query[0]: index.query(query[1])}
            evalu = queryevaluation(results, qrels1, query)

            data['query_no'] = query[0]
            data['query_text'] = query[1]
            data['prec@10'] = evalu.return_pratk(k_value)
            data['mean_average_precision'] = evalu.MAP(query[0])

            writer.writerow(data)

    pass

def pr_curve(index, queries, query_no):

	query_index = query_no - 851
	query = queries[query_index]
	results = {query[0]: index.query(query[1])}
	evalu = queryevaluation(results, qrels1, query)

	evalu.print_prcurve()



"""
Extract querys from the text file and add to query_array
Input: file address
Output: [[int(topicnumber), str(query)]]
"""
def extract_queries(url):
    query_text = open(url).read()
    title = re.compile(r"(?<=<title>\s).*")

    # starting number of the topic
    topic = 851
    query_array = []

    output = title.findall(query_text)

    for query in output:
        query_array.append((topic, query))
        topic += 1

    return query_array


# Run the Main Method
if __name__ == '__main__':
    main()
