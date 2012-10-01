from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from workflow.timemachine import cookie

register = template.Library()

@register.filter
def timeMachine_currentlyTraveling( request ):
	return cookie.currentlyTraveling( request )

@register.filter
def timeMachine_currentlyTravelingDateObject( request ):
	currentlyTravelingTo = cookie.currentlyTravelingTo( request )
	return mark_safe( "new Date( %s, %s, %s, %s, %s, %s )" % (
		currentlyTravelingTo.year,
		currentlyTravelingTo.month - 1,
		currentlyTravelingTo.day,
		currentlyTravelingTo.hour,
		currentlyTravelingTo.minute,
		currentlyTravelingTo.second ) )
