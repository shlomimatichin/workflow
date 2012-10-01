class Property:
	def __init__( self, name, regularExpression = None ):
		self.name = name
		self.regularExpression = regularExpression

class RequireProperty:
	def __init__( self, name ):
		self.name = name
