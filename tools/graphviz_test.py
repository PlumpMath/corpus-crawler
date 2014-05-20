import pydot
import ConfigParser
import sys

parser = ConfigParser.ConfigParser()
parser.optionxform=str
filein = sys.argv[1]
fileout = sys.argv[2]
parser.read(filein)
nodes = parser.options('TREE')
graph = pydot.Dot(graph_type='digraph', rankdir='LR')
for node in nodes:
    #graph.add_node(pydot.Node(node))
    children = parser.get('TREE', node)
    for child in children.split(' '):
        if(child != ""):
            edge = pydot.Edge(node, child)
            graph.add_edge(edge)
graph.write_png(fileout)