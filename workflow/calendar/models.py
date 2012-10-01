from django.db import models
from django.contrib.auth.models import User

class Attendance( models.Model ):
	date = models.DateField()
	teamMember = models.ForeignKey( User, blank = True, null = True, related_name = "calendarAttendances" )
	workingDay = models.BooleanField()
	user = models.ForeignKey( User, related_name = "calendarAttendancesReported" )
	when = models.DateTimeField( auto_now = True )

	def __unicode__( self ):
		return "<Attendance %s %s %s>" % ( self.date, self.teamMember.username if self.teamMember else 'team', self.workingDay )
