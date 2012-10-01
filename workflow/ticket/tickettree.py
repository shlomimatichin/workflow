from workflow.customworkflow import customworkflow
from workflow.ticket import models
import re

class TicketTree:
	_CATEGORY = re.compile( r'^/Category/([\w ]+)$' )
	_STATE = re.compile( r'^/State/([\w ]+)$' )
	_TICKET = re.compile( r'^/Ticket/(\d+)$' )

	def __init__( self, path ):
		if path == "/By Category":
			self._nodes = [ self._node( c.name, '/Category/' + c.name ) for c in customworkflow.CATEGORIES ]
		elif self._CATEGORY.search( path ) is not None:
			categoryName = self._CATEGORY.search( path ).group( 1 )
			category = next( c for c in customworkflow.CATEGORIES if c.name == categoryName )
			self._nodes = [ self._node( s.name, '/State/' + s.name ) for s in category.states ]
		elif self._STATE.search( path ) is not None:
			state = self._STATE.search( path ).group( 1 )
			tickets = [ t for t in models.Ticket.objects.all() if t.state() == state ]
			self._nodes = self._ticketsNodes( tickets ) 
		elif self._TICKET.search( path ) is not None:
			ticketID = self._TICKET.search( path ).group( 1 )
			ticket = models.Ticket.objects.get( id = ticketID )
			tickets = ticket.children()
			self._nodes = self._ticketsNodes( tickets ) 
		else:
			raise Exception( "Path '%s' in tree not coded yet" % path )

	def nodes( self ):
		return self._nodes

	def _ticketsNodes( self, tickets ):
		return [	self._node( t.title(),
					"/Ticket/%s" % t.id,
					ticket = t ) for t in tickets ]

	def _node( self, title, path, ticket = None ):
		result = {	"data" : title,
					"attr" : {	'data-path' : path,
								'id' : path.replace( ' ', '_' ).replace( '/', '_' ) },
					"state" : "closed" }
		if ticket:
			result[ 'attr' ][ 'data-ticket' ] = ticket.id
			result[ 'attr' ][ 'data-parents' ] = " ".join( str( t.id ) for t in ticket.parents() )
		return result
