import traceback

ENABLED = True

class PrintException:
	def __call__( self, method ):
		def _new( * args, ** kwargs ):
			try:
				return method( * args, ** kwargs )
			except:
				global ENABLED
				if ENABLED:
					traceback.print_exc( "Exception" )
				raise
		return _new
