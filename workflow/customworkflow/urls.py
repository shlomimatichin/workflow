from django.conf.urls.defaults import *

urlpatterns = patterns( 'workflow.customworkflow.views',
	( r'^plotStateMachine$', 'plotStateMachine' ),
	( r'^stateMachine$', 'stateMachine' ),
)
