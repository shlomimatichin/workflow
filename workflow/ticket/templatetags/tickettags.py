from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

register = template.Library()

@register.filter
def ticketAnchor_title( ticket ):
	result = '<a href="viewTicket?ticket=%d">Ticket %d: "%s"</a>' % (
			ticket.id, ticket.id, conditional_escape( ticket.title() ) )
	return mark_safe( result )

@register.filter
def ticketAnchor_titleState( ticket ):
	result = '<a href="viewTicket?ticket=%d">Ticket %d: "%s", %s</a>' % (
			ticket.id, ticket.id, conditional_escape( ticket.title() ), conditional_escape( ticket.state() ) )
	return mark_safe( result )

@register.filter
def ticketUserHistoryAnchor( user ):
	result = '<a href="viewHistory?user=%d">%s</a>' % ( user.id, conditional_escape( user.username ) )
	return mark_safe( result )
