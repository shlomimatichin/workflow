from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from workflow.customworkflow import plotstatemachine
from workflow import render
from workflow import debug
from django.conf import settings

@login_required
@debug.PrintException()
def plotStateMachine( request ):
	return HttpResponse( plotstatemachine.plotPNG(), mimetype = 'image/png' )

@login_required
@debug.PrintException()
def stateMachine( request ):
	return render.render( request, "customworkflow/statemachine.html", 
		states = open( settings.CUSTOM_WORKFLOW_MODULE.__file__.rstrip( 'co' ) ).read() )
