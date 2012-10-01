from workflow.timemachine import cookie
import threading
from django import shortcuts

localThreadStorage = threading.local()

class ExceptionWhileInTimeTravel:
	def __call__( self, method ):
		def _new( * args, ** kwargs ):
			if hasattr( localThreadStorage, 'currentlyTravelingTo' ):
				raise Exception( "Not allowed while in time travel" )
			return method( * args, ** kwargs )
		return _new

class TimeTravel:
	def __init__( self, allowedInTimeTravel = True ):
		self._allowedInTimeTravel = allowedInTimeTravel

	def __call__( self, method ):
		if not self._allowedInTimeTravel:
			def _new( request, * args, ** kwargs ):
				if cookie.currentlyTraveling( request ):
					return shortcuts.redirect( "/timemachine/notAllowedToChangePast" )
				assert not hasattr( localThreadStorage, 'currentlyTravelingTo' ) 
				return method( request, * args, ** kwargs )
			return _new

		def _new( request, * args, ** kwargs ):
			if cookie.currentlyTraveling( request ):
				localThreadStorage.currentlyTravelingTo = cookie.currentlyTravelingTo( request )
				try:
					return method( request, * args, ** kwargs )
				finally:
					del localThreadStorage.currentlyTravelingTo
			else:
				assert not hasattr( localThreadStorage, 'currentlyTravelingTo' ) 
				return method( request, * args, ** kwargs )
		return _new
