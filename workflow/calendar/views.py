from django.contrib.auth.decorators import login_required
import datetime
import calendar
import time
from django.http import HttpResponseRedirect, HttpResponse
from workflow import render
from django.conf import settings
from workflow.calendar import models
from workflow.timemachine import timemachine
from django import shortcuts
import collections

_MONTH_NAMES = [ "January", "February", "March", "April", "May", "June",
					"July", "August", "September", "October", "November", "December" ]
_DAY_NAMES = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]

@login_required
def years( request, year = None ):
	if year:
		year = int(year)
	else:
		year = time.localtime()[0]

	nowy, nowm = time.localtime()[:2]
	lst = []

	for y in [year, year+1]:
		mlst = []
		for n, month in enumerate(_MONTH_NAMES):
			current = False
			if y == nowy and n+1 == nowm:
				current = True
			mlst.append( dict( n = n + 1, name = month, current = current ) )
		lst.append((y, mlst))

	return render.render( request, "calendar/years.html", years = lst, year = year )

def _isWorkingDay( date ):
	nonTeamAttendances = list( timemachine.filter(
			models.Attendance.objects.filter( date = date, teamMember__isnull = True ) ) )
	if len( nonTeamAttendances ) == 0:
		return settings.WEEKDAY_IS_WORKING_DAY( date.weekday() )
	else:
		return nonTeamAttendances[ -1 ].workingDay

def _teamMemberWorking( member, date ):
	attendances = list( timemachine.filter(
			models.Attendance.objects.filter( date = date, teamMember = member ) ) )
	if len( attendances ) == 0:
		return _isWorkingDay( date )
	else:
		return attendances[ -1 ].workingDay

def _dateExceptions( date ):
	teamAttendances = timemachine.filter( models.Attendance.objects.filter(
		date = date, teamMember__isnull = False ) )
	result = collections.OrderedDict()
	for attendance in teamAttendances:
		result[ attendance.user.username ] = attendance.workingDay
	workingDay = _isWorkingDay( date )
	return list( x for x in result.iteritems() if x[ 1 ] != workingDay )

@login_required
@timemachine.decorators.TimeTravel()
def month( request, year, month, change = None ):
	year = int( year )
	month = int( month )

	if change in ( "next", "prev" ):
		monthStart = datetime.date( year, month, 1 )
		if change == "next":
			monthStart += datetime.timedelta( days = 31 )
		else:
			monthStart -= datetime.timedelta( days = 1 )
		year, month = monthStart.timetuple()[ : 2 ]

	cal = calendar.Calendar( settings.CALENDAR_FIRST_WEEKDAY )
	today = datetime.date.today()
	dayTitles = [ _DAY_NAMES[ d ] for d in cal.iterweekdays() ]
	rows = [ [] ]
	users = list( models.User.objects.all() )

	for date in cal.itermonthdates( year, month ):
		if len( rows[ -1 ] ) >= 7:
			rows.append( [] )
		classes = ""
		text = ""
		if date.month == month:
			classes += " dayInMonthTable_ThisMonth"
		else:
			classes += " dayInMonthTable_NotThisMonth"
		if _isWorkingDay( date ):
			classes += " dayInMonthTable_WorkingDay"
			text += "Working day"
		else:
			classes += " dayInMonthTable_NonWorkingDay"
			text += "Non working day"
		if date == today:
			classes += " dayInMonthTable_Today"
			text = "Today, " + text
		rows[ -1 ].append( ( date, classes, text, _dateExceptions( date ) ) )

	return render.render( request, "calendar/month.html",
				year = year,
				month = month,
				dayTitles = dayTitles,
				rows = rows,
				users = users,
				mname = _MONTH_NAMES[ month - 1 ] )

@login_required
@timemachine.decorators.TimeTravel( allowedInTimeTravel = False )
def toggleWorkingDay( request, year, month, day ):
	date = datetime.date( int( year ), int( month ), int( day ) )
	attendance = models.Attendance( date = date, workingDay = not _isWorkingDay( date ), user = request.user )
	attendance.save()
	return shortcuts.redirect( "/calendar/month/%s/%s" % ( year, month ) )

@login_required
@timemachine.decorators.TimeTravel( allowedInTimeTravel = False )
def toggleTeamMember( request, id, year, month, day ):
	teamMember = models.User.objects.get( id = id )
	date = datetime.date( int( year ), int( month ), int( day ) )
	attendance = models.Attendance(	date = date,
									teamMember = teamMember,
									workingDay = not _teamMemberWorking( teamMember, date ),
									user = request.user )
	attendance.save()
	return shortcuts.redirect( "/calendar/month/%s/%s" % ( year, month ) )
