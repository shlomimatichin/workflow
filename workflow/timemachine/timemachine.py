from workflow.timemachine import cookie
from workflow.timemachine import decorators

def filter( querySet ):
	if not hasattr( decorators.localThreadStorage, 'currentlyTravelingTo' ):
		return querySet
	return querySet.filter( when__lt = decorators.localThreadStorage.currentlyTravelingTo )
