from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators import cache
from workflow.ticket import forms
from workflow.ticket import models
from workflow.ticket import tickettree
import pprint
from django import shortcuts
import json
from django.views.decorators import csrf
from workflow import debug
from workflow import render

from workflow.customworkflow import customworkflow
from django.conf import settings
from workflow.timemachine import timemachine

def _lastViewedTickets( request ):
	result = []
	if request.COOKIES.has_key( 'lastViewedTickets' ):
		for id in json.loads( request.COOKIES[ 'lastViewedTickets' ] ):
			try:
				result.append( models.Ticket.objects.get( id = id ) )
			except:
				pass
	return result

def _render( request, template, lastViewedTickets = None, ** kwargs ):
	if lastViewedTickets is None:
		lastViewedTickets = _lastViewedTickets( request )
	kwargs[ 'lastViewedTickets' ] = reversed( lastViewedTickets )
	return render.render( request, "ticket/" + template, ** kwargs )

@login_required
@cache.never_cache
@debug.PrintException()
@timemachine.decorators.TimeTravel()
def index(request):
	return _render( request, 'index.html' )

@login_required
@debug.PrintException()
@timemachine.decorators.TimeTravel()
def viewHistory( request ):
	return _render( request, 'viewhistory.html', 
		limitToUser = request.REQUEST.get( 'user', None ) )

@login_required
@debug.PrintException()
@timemachine.decorators.TimeTravel( allowedInTimeTravel = False )
def newTicket( request ):
	if request.method == 'POST':
		form = forms.NewTicket( request.POST )
		if form.is_valid():
			ticket = models.Ticket.create()
			ticket.setProperty( name = 'Title', value = form.cleaned_data[ 'title' ], user = request.user )
			ticket.setProperty( name = 'State', value = form.cleaned_data[ 'state' ], user = request.user )
			return HttpResponseRedirect( 'viewTicket?ticket=%s' % ticket.id )
	else:
		form = forms.NewTicket()
	return _render( request, 'newticket.html',
		form = form,
		tickettypes = [ s for s in customworkflow.ALL_STATES if s.showAsNew ] )

@login_required
@debug.PrintException()
@timemachine.decorators.TimeTravel()
def viewTicket( request ):
	ticket = models.Ticket.objects.get( id = request.REQUEST[ 'ticket' ] )
	if ticket.state() == "No state":
		return _render( request, 'viewticketfromthefuture.html', ticket = ticket )

	transitions = [ '<li><a href="doTransition?ticket=%d&transition=%s">%s</a></li>' % ( ticket.id, t.name, t.name )
					for t in customworkflow.STATE_MAP[ ticket.state() ].transitions() ]
	spawnChilds = [ '<li><a href="doSpawnChild?ticket=%d&spawnchild=%s">%s</a></li>' % ( ticket.id, s.name, s.name )
					for s in customworkflow.STATE_MAP[ ticket.state() ].spawnChilds ]
	devider = [ '<li class="divider"></li>' ]
	discard = [ '<li><a href="doTransition?ticket=%d&transition=Discard">Discard</a></li>' % ticket.id ]
	actions = "\n".join( transitions + spawnChilds + devider + discard )

	titleProperty = [ '<li><a href="setProperty?ticket=%d&property=Title">Title</a></li>' % ticket.id ]
	stateProperty = [ '<li><a href="setProperty?ticket=%d&property=State">State</a></li>' % ticket.id ]
	customProperties = [ '<li><a href="setProperty?ticket=%d&property=%s">%s</a></li>' % (
			ticket.id, p.name, p.name ) for p in customworkflow.PROPERTIES ]
	properties = "\n".join( titleProperty + stateProperty + devider + customProperties )

	lastViewedTickets = _lastViewedTickets( request )
	if ticket in lastViewedTickets:
		lastViewedTickets.remove( ticket )
	lastViewedTickets.append( ticket )
	lastViewedTickets = lastViewedTickets[ -10 : ]

	response = _render( request, 'viewticket.html',
		ticket = ticket,
		actions = actions,
		properties = properties,
		lastViewedTickets = lastViewedTickets )

	response.set_cookie( 'lastViewedTickets', json.dumps( [ t.id for t in lastViewedTickets ] ) )

	return response

@login_required
@debug.PrintException()
@timemachine.decorators.TimeTravel()
def getHistory( request ):
	ticketFilters = {}
	if 'ticket' in request.REQUEST:
		ticketFilters[ 'ticket' ] = models.Ticket.objects.get( id = request.REQUEST[ 'ticket' ] )
	if 'user' in request.REQUEST:
		ticketFilters[ 'user' ] = models.User.objects.get( id = request.REQUEST[ 'user' ] )
	properties = list( timemachine.filter( models.Property.objects.filter( ** ticketFilters ) ) )

	if 'ticket' in request.REQUEST:
		relationsTo = timemachine.filter( models.Relation.objects.filter( ticket = request.REQUEST[ 'ticket' ] ) )
		relationsFrom = timemachine.filter( models.Relation.objects.filter( relatedTo = request.REQUEST[ 'ticket' ] ) )
		relations = list( relationsTo ) + list( relationsFrom )
	else:
		relations = list( timemachine.filter( models.Relation.objects.all() ) )
	events = properties + relations
	events.sort( key = lambda x: x.when, reverse = True )
	page = int( request.REQUEST.get( 'page', 0 ) )
	PAGE_SIZE = 100
	first = page * PAGE_SIZE
	bound = first + PAGE_SIZE
	moreHistoryData = json.dumps( dict( request.REQUEST, page = page + 1 ) ) if bound < len( events ) else ""
	paged = events[ first : bound ]
	return _render( request, 'history.html', events = paged, moreHistoryData = moreHistoryData )

@login_required
@debug.PrintException()
@timemachine.decorators.TimeTravel( allowedInTimeTravel = False )
def doTransition( request ):
	ticket = models.Ticket.objects.get( id = request.REQUEST[ 'ticket' ] )
	transitionName = str( request.REQUEST[ 'transition' ] )
	if transitionName == "Discard":
		targetState = "Discarded"
	else:
		transition = customworkflow.STATE_MAP[ ticket.state() ].transitionByName( request.REQUEST[ 'transition' ] )
		targetState = transition.targetState
	ticket.setProperty( name = 'State', value = targetState, user = request.user )
	return HttpResponseRedirect( 'viewTicket?ticket=%s' % ticket.id )

@login_required
@cache.never_cache
@debug.PrintException()
def findTicket( request ):
	return _render( request, 'findticket.html' )

@csrf.csrf_exempt
@login_required
@cache.never_cache
@debug.PrintException()
@timemachine.decorators.TimeTravel()
def searchTicketByFreeText( request ):
	term = request.REQUEST[ 'term' ]
	properties = list( timemachine.filter( models.Property.objects.filter( value__contains = term ) ) )
	result = [ dict(	label = "%s: %s" %( p.name, p.value ),
						value = "viewTicket?ticket=%d" % p.ticket.id )
					for p in properties[ -10 : ] ]
	return HttpResponse( json.dumps( result ), mimetype = "application/json" )

@login_required
@cache.never_cache
@debug.PrintException()
@timemachine.decorators.TimeTravel()
def ticketTree( request ):
	if 'path' in request.REQUEST:
		result = tickettree.TicketTree( request.REQUEST[ 'path' ] ).nodes()
		return HttpResponse( json.dumps( result ), mimetype = "application/json" )
	else:
		return _render( request, 'tickettree.html', user = request.user )

@login_required
@cache.never_cache
@debug.PrintException()
@timemachine.decorators.TimeTravel( allowedInTimeTravel = False )
def setRelation( request ):
	name = request.REQUEST[ 'name' ]
	assert name in [ 'Parent Of', 'Not Parent Of' ]
	ticket = models.Ticket.objects.get( id = request.REQUEST[ 'ticket' ] )
	relatedTo = models.Ticket.objects.get( id = request.REQUEST[ 'relatedTo' ] )
	assert ticket != relatedTo
	assert name != 'Parent Of' or relatedTo not in ticket.children()
	assert name != 'Not Parent Of' or relatedTo in ticket.children()
	ticket.addRelationAtEnd( name, relatedTo, request.user )
	if 'redirectToViewTicket' in request.REQUEST:
		return HttpResponseRedirect( 'viewTicket?ticket=%s' % request.REQUEST[ 'redirectToViewTicket' ] )
	else:
		return HttpResponse( '' )

@login_required
@cache.never_cache
@debug.PrintException()
@timemachine.decorators.TimeTravel( allowedInTimeTravel = False )
def reorderRelation( request ):
	name = request.REQUEST[ 'name' ]
	assert not name.startswith( 'Not ' )
	ticket = models.Ticket.objects.get( id = request.REQUEST[ 'ticket' ] )
	relations = ticket.relations( request.REQUEST[ 'name' ] )
	order = [ int( o ) for o in request.REQUEST.getlist( 'order[]' ) ]
	assert len( order ) == len( relations )
	reorderedTicket = models.Ticket.objects.get( id = request.REQUEST[ 'reorderedTicket' ] )
	assert reorderedTicket in [ r.relatedTo for r in relations ]

	newOrder = order.index( reorderedTicket.id )
	previousID = order[ newOrder - 1 ] if newOrder > 0 else None
	nextID = order[ newOrder + 1 ] if newOrder < len( order ) - 1 else None
	findOrderByID = lambda id: [ r for r in relations if r.relatedTo.id == id ][ 0 ].order
	if previousID and nextID:
		orderValue = ( findOrderByID( nextID ) + findOrderByID( previousID ) ) / 2
	elif previousID:
		orderValue = findOrderByID( previousID ) + 1
	else:
		assert nextID
		orderValue = findOrderByID( nextID ) - 1

	ticket.addRelation( name, reorderedTicket, orderValue, request.user )

	if 'redirectToViewTicket' in request.REQUEST:
		return HttpResponseRedirect( 'viewTicket?ticket=%s' % request.REQUEST[ 'redirectToViewTicket' ] )
	else:
		return HttpResponse( '' )

@login_required
@debug.PrintException()
@timemachine.decorators.TimeTravel( allowedInTimeTravel = False )
def setProperty( request ):
	ticket = models.Ticket.objects.get( id = request.REQUEST[ 'ticket' ] )
	FormClass = forms.SetStateProperty if str( request.REQUEST[ 'property' ] ) == "State" else forms.SetProperty
	if request.method == 'POST':
		form = FormClass( request.POST )
		if form.is_valid():
			ticket.setProperty( name = form.cleaned_data[ 'property' ],
								value = form.cleaned_data[ 'value' ],
								user = request.user )
			return HttpResponseRedirect( 'viewTicket?ticket=%s' % ticket.id )
	else:
		initial = dict( request.REQUEST, value = ticket.getPropertyValue( request.REQUEST[ 'property' ], '' ) )
		form = FormClass( initial = initial )
	return _render( request, 'setproperty.html', form = form )

@login_required
@debug.PrintException()
@timemachine.decorators.TimeTravel( allowedInTimeTravel = False )
def doSpawnChild( request ):
	parentTicket = models.Ticket.objects.get( id = request.REQUEST[ 'ticket' ] )
	if request.method == 'POST':
		form = forms.SpawnChild( request.POST )
		if form.is_valid():
			ticket = models.Ticket.create()
			ticket.setProperty( name = 'Title', value = form.cleaned_data[ 'title' ], user = request.user )
			ticket.setProperty( name = 'State', value = form.cleaned_data[ 'state' ], user = request.user )
			parentTicket.addRelationAtEnd( 'Parent Of', ticket, request.user )
			return HttpResponseRedirect( 'viewTicket?ticket=%s' % ticket.id )
	else:
		spawnChild = customworkflow.STATE_MAP[ parentTicket.state() ].spawnChildByName( request.REQUEST[ 'spawnchild' ] )
		initial = dict( request.REQUEST, state = spawnChild.childState )
		form = forms.SpawnChild( initial = initial )
	return _render( request, 'dospawnchild.html', form = form )
