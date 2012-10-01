from django.contrib.auth.decorators import login_required
from workflow import render
from django.conf import settings
import datetime
from workflow.timemachine import cookie
from django import shortcuts

@login_required
def index( request ):
	return render.render( request, "timemachine/index.html",
			dateFormat = settings.TIMEMACHINE_DATEPICKET_DATE_FORMAT,
			hours = range( 24 ),
			minutes = range( 60 ) )

@login_required
def notAllowedToChangePast( request ):
	return render.render( request, "timemachine/notallowedtochangepast.html" )

@login_required
def travelToDate( request, year, month, day ):
	response = shortcuts.redirect( "/timemachine" )
	when = datetime.datetime( int( year ), int( month ), int( day ), 23, 59, 59 )
	return cookie.travelToDate( response, when )

@login_required
def travelToPresent( request ):
	response = shortcuts.redirect( "/timemachine" )
	return cookie.travelToPresent( response )

@login_required
def travelToHour( request, hour ):
	response = shortcuts.redirect( "/timemachine" )
	currently = cookie.currentlyTravelingTo( request )
	when = datetime.datetime.combine( currently.date(), datetime.time( int( hour ), currently.minute, 59 ) )
	return cookie.travelToDateTime( response, when )

@login_required
def travelToMinute( request, minute ):
	response = shortcuts.redirect( "/timemachine" )
	currently = cookie.currentlyTravelingTo( request )
	when = datetime.datetime.combine( currently.date(), datetime.time( currently.hour, int( minute ), 59 ) )
	return cookie.travelToDateTime( response, when )
