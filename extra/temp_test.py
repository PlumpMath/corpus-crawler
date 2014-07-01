import pydot
import ConfigParser
import sys

parser = ConfigParser.ConfigParser()
parser.optionxform=str
filein = sys.argv[1]
fileout = sys.argv[2]
phrase = sys.argv[3]
parser.read(filein)
print parser.sections()
nodes = parser.options('TREE')
print len(nodes)
graph = pydot.Dot(graph_type='digraph', rankdir='LR')
for node in nodes:
	if "logger" in node:
	    #graph.add_node(pydot.Node(node))
	    print node
	    children = parser.get('TREE', node)
	    for child in children.split(' '):
	        if(child != ""):
	            edge = pydot.Edge(node, child)
	            graph.add_edge(edge)
graph.write_png(fileout)