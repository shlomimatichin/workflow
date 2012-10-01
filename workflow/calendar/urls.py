from django.conf.urls.defaults import *

urlpatterns = patterns( 'workflow.calendar.views',
	( r"^years/(\d+)/$", "years" ),
	( r"^$", "years" ),

	( r"^month/(\d+)/(\d+)/(prev|next)/$", "month" ),
	( r"^month/(\d+)/(\d+)/$", "month" ),
	( r"^month$", "month" ),

	( r"^toggleWorkingDay/(\d+)/(\d+)/(\d+)$", "toggleWorkingDay" ),
	( r"^toggleTeamMember/(\d+)/(\d+)/(\d+)/(\d+)$", "toggleTeamMember" ),
)
