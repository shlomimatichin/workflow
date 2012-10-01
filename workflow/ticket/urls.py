from django.conf.urls.defaults import *

urlpatterns = patterns( 'workflow.ticket.views',
	( r'^$', 'index' ),
	( r'^newTicket$', 'newTicket' ),
	( r'^viewTicket$', 'viewTicket' ),
	( r'^viewHistory$', 'viewHistory' ),
	( r'^findTicket$', 'findTicket' ),
	( r'^ticketTree$', 'ticketTree' ),

	( r'^getHistory$', 'getHistory' ),
	( r'^doTransition$', 'doTransition' ),
	( r'^doSpawnChild$', 'doSpawnChild' ),
	( r'^setProperty$', 'setProperty' ),
	( r'^setRelation$', 'setRelation' ),

	( r'^searchTicketByFreeText$', 'searchTicketByFreeText' ),
)
