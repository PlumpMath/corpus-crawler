from rdflib import RDFS, URIRef, Graph, RDF
import rdflib.Namespace
import ConfigParser
import sys

filein = sys.argv[1]
fileout = open( sys.argv[2], 'w' )

# setup OWL as the owl namespace.  The built in rdflib OWL namespace (like RDF and RDFS) doesn't work, so we do it manually.
OWL = rdflib.Namespace('http://www.w3.org/2002/07/owl#')

# We use the ConfigParser to convert the python config file to an OWL file.

parser = ConfigParser.ConfigParser()
parser.optionxform=str
parser.read( filein )

g = Graph()

nodes = parser.options( 'TREE' )
for node in nodes:
	if( '%' not in node and '|' not in node ):
		node_name = node.replace("'","")
		node_name = node_name.replace("`","_")
		node_name = node_name.replace(">","")
		node_name = node_name.replace("<","")
		node_name = node_name.replace("#","")	
		node_uri = "http://troxel/corpuscrawler/entity/" + node_name
		node_ref = URIRef( node_uri )
		g.add( ( node_ref, RDF.type, OWL.Class ) )
		children = parser.get( 'TREE', node )
		for child in children.split( ' ' ):
			if( child != "" and '%' not in child and '|' not in child ):
				child = child.replace("'","")
				child = child.replace("`","_")
				child = child.replace(">","")
				child = child.replace("<","")
				child = child.replace("#","")		
				child_uri = "http://troxel/corpuscrawler/entity/" + child
				child_ref = URIRef( child_uri )
				g.add( ( child_ref, RDF.type, OWL.Class ) )
				g.add( ( child_ref, RDFS.subClassOf, node_ref ) )

# this line allow the .owl file to show "owl:some-rdf" 
g.bind("owl", OWL)

#pretty print of xml is required for owl to show up right
fileout.write( g.serialize( format='pretty-xml') )
fileout.close()