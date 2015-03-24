

from glob import glob

directory = "/Users/lukejones/Desktop/University/web_search_and_text_analysis/proj1data/blogs/*.txt"

corpus = []

for document in glob(directory):

	doc = open(document, "r").read()
	corpus.append(doc)

print "No. Docs {0:n}".format(len(corpus))

print corpus