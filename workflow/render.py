from django import shortcuts

def render( request, template, ** kwargs ):
	kwargs[ 'request' ] = request
	return shortcuts.render( request, template, kwargs )
