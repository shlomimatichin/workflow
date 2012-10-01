from workflow.customworkflow import customworkflow 
import pygraphviz

def plotPNG():
	graph = pygraphviz.AGraph( directed = True, strict = False )
	for state in customworkflow.ALL_STATES:
		graph.add_node( state.name, shape = state.plotShape )
	for state in customworkflow.ALL_STATES:
		for transition in state.transitions():
			graph.add_edge( state.name, transition.targetState, label = transition.name )
		for spawnChild in state.spawnChilds:
			graph.add_edge( state.name, spawnChild.childState, label = spawnChild.name, style = 'dotted' )
	graph.layout( 'dot' )
	return graph.draw( path = None, format = "png" )

if __name__ == "__main__":
	open( "/tmp/test.png", "wb" ).write( plotPNG() )
