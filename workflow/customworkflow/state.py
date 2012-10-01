from workflow.customworkflow.transition import Transition
from workflow.customworkflow.spawnchild import SpawnChild
from workflow.customworkflow.property import RequireProperty 
import itertools

class State:
	def __init__( self, name, * all, ** kwargs ):
		self.name = name
		self.showAsNew = kwargs.get( 'showAsNew', False )
		self.plotShape = kwargs.get( 'plotShape', 'ellipse' )

		self.nonCategoryTransitions = [ t for t in all if isinstance( t, Transition ) ]
		self.spawnChilds = [ s for s in all if isinstance( s, SpawnChild ) ]
		self.requiredProperties = [ r for r in all if isinstance( r, RequireProperty ) ]

		assert len( self.nonCategoryTransitions ) + len( self.spawnChilds ) + len( self.requiredProperties ) == len( all )

		self.categoryTransitions = []

	def transitions( self ):
		return itertools.chain( self.nonCategoryTransitions, self.categoryTransitions )

	def transitionByName( self, name ):
		name = str( name )
		for transition in self.transitions():
			if transition.name == name:
				return transition
		raise KeyError( "No transition named '%s'" % name )

	def spawnChildByName( self, name ):
		name = str( name )
		for spawnChild in self.spawnChilds:
			if spawnChild.name == name:
				return spawnChild
		raise KeyError( "No spawn child named '%s'" % name )
