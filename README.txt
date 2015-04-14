___________________________________________________________________________________________________
PYTHON IMPLEMENTATION OF AN INVERTED INDEX WITH POSITIONAL INDICES AND EVALUATION CLASS
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 14 April 2015
___________________________________________________________________________________________________

This readme file outlines how to use the inverted index package. The package contains three files;
1) An inverted index class
2) An evaluation class
3) A queries class which allows the user to implement the first two classes

NOTE: You MUST make some minor amendments to queries.py for the package to work as intended (refer to section 3).

To run the index using a command line tool, navigate to the directory containing the package.
Enter the command: python queries.py

The software should then run as intended.

“””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””
1) INVERTED INDEX CLASS
creates an inverted index in the form of:
index = {'token': [IDF, {'documentID': [posting1, posting2, posting_i]}]}
document = {‘DocID’:|w,d|}

Key functions include:
build_index(corpus)
Used to build an index. General usage is as follows;

#constructor
index = invertedindex()

#build index
index.build_index(corpus)
	
Input: corpus = "/directory/subdirectory/*.txt"
Output:	Inverted index object, updated with corpus

write_index to file(index, documents)
Used to save the index to file to save unnecessary processing time.
Input: URL for index and documents in the form of "/directory/subdirectory/*.pkl"
Output: .pkl file for index and documents

load_index(index, documents)
Used to load a saved index
Input: URL for index and documents in the form of "/directory/subdirectory/*.pkl"
Output: Updated inverted index object

query(query)
Used to query the index and retrieve ranked results. 

index.query('web search and text analysis')

Input: Query as a string
Method: Check for phrase query
	If phrase query:
	 	then reduce documents to subset containing phrasequery
		Sum the results of TF x IDF for each document
		Normalise by dividing by the length of the document
	Else: 
		Sum the results of TF x IDF for each document
		Normalise by dividing by the length of the document
Output: Ranked results
Return: {DocID: score}

It is important to note that results are returned as a dictionary.


“””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””
2) QUERY EVALUATION CLASS
Used to evaluate the performance of an information retrieval system

Inputs:
Ranked results: {querynumber: {documentID: rank_score}}
Query relevance: space deliminated text file in form of: <query number> <number> <documentID> <relevance>
Total relevant results: int (number of relevant documents)
Query number: int (reference number of the query)

#example constructor
evalu = queryevaluation(ranked_results, qrels, query)

Methods: 
MAP: returns mean average precision for a given query
MAP(query_no)

Print P-R Curve: Prints the P-R curve for a given query
print_prcurve()

Precision@k: Returns the precision at k
return_pratk(k=10)

“””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””””
3) QUERY FILE
Contains a number of functions to implement both the previous classes.

extract_queries(url)
Used to extract the queries from the query file '06.topics.851-900.txt'
Returns: [(topic_no., 'query')]

ranked_results(index, query, k = 10):
Prints k ranked results to the screen for a give query

write_results(index, queries, qrels, outputfile)
Writes results to a CSV file in the form of:
'query_no','query_text','prec@10','mean_average_precision'
Inputs: index object, queries (extracted), qrels as a space deliminated text file in form of: <query number> <number> <documentID> <relevance> and a url to an outputfile (use .csv)

pr_curve(index, queries, qrels, query_no)
Basic extension on the print_prcurve() method in the Query Evaluation Object
Lets the user enter a index, query array (i.e. output from extract queries)
and a query number and prints the PR Curve to the screen.
Inputs as per above.

EXAMPLE USES

#Build an index and write to file
index = invertedindex()
index.build_index(corpus)
index.write_index_to_file(saved_index, saved_documents)

#Load an index, run test queries through it and write the results to file
queries = extract_queries(queryfile)
index = invertedindex()
index.load_index(saved_index, saved_documents)
write_results(index, queries, output_file)

#Load an index, display ranked results for the term 'audi' and print its pr_curve
queries = extract_queries(queryfile)
index = invertedindex()
index.load_index(saved_index, saved_documents)
ranked_results(index, 'audi', 10)
pr_curve(index, queries, 888)
