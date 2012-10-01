import datetime

_FORMAT = "%Y-%m-%dT%H:%M:%S"

def currentlyTraveling( request ):
	return request.COOKIES.has_key( 'timemachine' )

def currentlyTravelingTo( request ):
	if not currentlyTraveling( request ):
		return None
	return datetime.datetime.strptime( request.COOKIES[ 'timemachine' ], _FORMAT )

def travelToPresent( response ):
	response.delete_cookie( 'timemachine' )
	return response

def travelToDate( response, date ):
	when = datetime.datetime.combine( date, datetime.time( 23, 59, 59 ) ) 
	return travelToDateTime( response, when )

def travelToDateTime( response, when ):
	response.set_cookie( 'timemachine', when.strftime( _FORMAT ) )
	return response
