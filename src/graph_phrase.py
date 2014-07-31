import pydot
import ConfigParser
import sys

running = True
while(running):
	phrase = str(raw_input("PHRASE: "))
	fileout = "graph_" + phrase + ".png"
	parser = ConfigParser.ConfigParser()
	parser.optionxform=str
	filein = sys.argv[1]
	#fileout = sys.argv[2]
	#phrase = sys.argv[3]
	parser.read(filein)
	nodes = parser.options('TREE')
	graph = pydot.Dot(graph_type='digraph')
	for node in nodes:
		if phrase in node or phrase == node:
		    #graph.add_node(pydot.Node(node))
		    children = parser.get('TREE', node)
		    for child in children.split(' '):
		        if(child != ""):
		            edge = pydot.Edge(node, child)
		            graph.add_edge(edge)
	graph.write_png(fileout)