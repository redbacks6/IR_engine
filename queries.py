"""
Query Processor
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 24 March 2015
"""

import re 
from pprint import pprint as pp

url = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/06.topics.851-900.txt'



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

	pp(query_array)
