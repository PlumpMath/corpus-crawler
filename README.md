corpuscrawler
=============

Interop Grant Project, Summer 2014.

To use this tool, you must have the python libraries for NLTK, RDFLIB, and PYDOT downloaded.
Files in the src/ directory are finished and ready for use.
Files in the extra/ directory are beta versions, and include various test files.

To "crawl" a directory, start the "init.py" file.
Use the command "crawl" to crawl the loaded corpus and grab all the words from the sentences.
Use the command "tocsv" to convert the word (phrase) list to a CSV file, complete with file name and location in file.
Use the command "metrics" to convert the csv file to file with the given metrics for each word. These metrics include total count for each phrase, and the most common file location.

The "generate_graph_file.py" script generates a python Config file representing the graph of the phrases in the metrics file. Syntax is "python generate_graph_file.py <metric-file> <output-file>".

The "graph_phrase.py" script allows one to generate graphviz (.png) files from the config file previously generated.  Syntax is "python graph_phrase.py <config-file>".
Enter the phrase you want at the root, and the file generates.

Last, the "generate_owl_file.py" script turns the config file into an OWL file.  Likely, the config file should be removed, but in the course of designing these scripts, this was unnecessary. Syntax is "python generate_owl_file.py <config-file> <output-owl-file>".