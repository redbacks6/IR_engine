"""
Query Processor
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 24 March 2015
"""

import re

url = '/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/06.topics.851-900.txt'

query_text = open(url).read()

number = re.compile(r"(?<=Number:\s).*")
title = re.compile(r"(?<=<title>\s).*")

#starting number of the topic
topic = 851

query_array = []

print query_text

if title.search(query_text):
	query_array.append((topic,title.search(query_text)))
	topic += 1

print query_array	
