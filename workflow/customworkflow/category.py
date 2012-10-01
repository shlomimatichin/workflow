from workflow.customworkflow.state import State
from workflow.customworkflow.transition import Transition

class Category:
	def __init__( self, name, * all ):
		self.name = name
		self.states = [ s for s in all if isinstance( s, State ) ]
		self.transitions = [ t for t in all if isinstance( t, Transition ) ]
		assert len( self.states ) + len( self.transitions ) == len( all ), \
				'Category contains member that is not a state, and not a transition: %s' % name

		for state in self.states:
			state.categoryTransitions = self.transitions
