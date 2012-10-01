from django.conf.urls.defaults import *

urlpatterns = patterns( 'workflow.timemachine.views',
	( r'^$', 'index' ),
	( r'^notAllowedToChangePast$', 'notAllowedToChangePast' ),
	( r'^travelToDate/(\d+)/(\d+)/(\d+)$', 'travelToDate' ),
	( r'^travelToHour/(\d+)$', 'travelToHour' ),
	( r'^travelToMinute/(\d+)$', 'travelToMinute' ),
	( r'^travelToPresent$', 'travelToPresent' ),
)
