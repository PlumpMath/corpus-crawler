import OWLify
import ConfigParser
import sys

_manager = OWLify.OWL( "http://jtroxel/corpuscrawler/entity", sys.argv[2], "http://jtroxel/corpuscrawler/prop" )

filein = sys.argv[1]

parser = ConfigParser.ConfigParser()
parser.optionxform=str
parser.read( filein )

nodes = parser.options( 'TREE' )
for node in nodes:
	if( '%' not in node and '|' not in node ):
		_manager.addClass( node )
		children = parser.get( 'TREE', node )
		for child in children.split( ' ' ):
			if( child != "" and '%' not in child and '|' not in child ):
				child = child.replace("'","")
				child = child.replace("`","_")
				child = child.replace(">","")
				child = child.replace("<","")
				child = child.replace("#","")				
				_manager.addClass( child )
				_manager.addSubClass( child, node )

_manager.end()