from django.conf import settings

CATEGORIES = settings.CUSTOM_WORKFLOW_STATES
ALL_STATES = sum( [ c.states for c in CATEGORIES ], [] )
ALL_STATE_NAMES = [ s.name for s in ALL_STATES ]
STATE_MAP = { s.name: s for s in ALL_STATES }
STATE_MAP.update( { unicode( s.name ): s for s in ALL_STATES } )
PROPERTIES = settings.CUSTOM_WORKFLOW_PROPERTIES

assert len( set( ALL_STATE_NAMES ) ) == len( ALL_STATE_NAMES ), 'Custom workflow error: a state name is used twice'
for state in ALL_STATES:
	for transition in state.transitions():
		assert transition.targetState in ALL_STATE_NAMES, "Transition %s, to state %s, is not in state list" % (
				transition.name, transition.targetState )
assert 'Discarded' in ALL_STATE_NAMES, 'The state "Discarded" must be defined'
