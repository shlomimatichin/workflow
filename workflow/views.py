from django.contrib.auth.decorators import login_required
from workflow import debug
from workflow import render

@login_required
@debug.PrintException()
def welcome( request ):
	return render.render( request, 'welcome.html' )
