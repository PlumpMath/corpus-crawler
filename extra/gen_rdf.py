from rdflib import RDFS, URIRef, Graph, RDF
import rdflib.Namespace
import ConfigParser
import sys

filein = sys.argv[1]
fileout = open( sys.argv[2], 'w' )

OWL = rdflib.Namespace('http://www.w3.org/2002/07/owl#')


parser = ConfigParser.ConfigParser()
parser.optionxform=str
parser.read( filein )

g = Graph()

nodes = parser.options( 'TREE' )
for node in nodes:
	if( '%' not in node and '|' not in node ):
		node_uri = "http://troxel/corpuscrawler/entity/" + node
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

g.bind("owl", OWL)

fileout.write( g.serialize( format='pretty-xml') )
fileout.close()