from django.db import models
import collections
from django.contrib.auth.models import User

from django.core import validators
from django.utils.translation import ugettext_lazy as _
import re
from workflow import timemachine
from workflow.timemachine import timemachine

validateWord = validators.RegexValidator(
				re.compile( r'^[-\w ]+$' ),
				_(u"Enter a valid 'slug' consisting of letters, numbers, spaces, underscores or hyphens."),
				'invalid' )

class Ticket( models.Model ):
	def __unicode__( self ):
		return "<Ticket %d: %s>" % ( self.id, self.title() )

	def title( self ):
		return self.getPropertyValue( 'Title', 'No title' )

	def state( self ):
		return self.getPropertyValue( 'State', 'No state' )

	def titleState( self ):
		return '"%s" [%s]' % ( self.title(), self.state() )

	@classmethod
	def create( cls ):
		self = cls()
		self.save()
		return self

	@timemachine.decorators.ExceptionWhileInTimeTravel()
	def setProperty( self, name, value, user ):
		prop = Property( ticket = self, name = name, value = value, user = user )
		prop.save()
		return prop

	def propertiesWithoutDups( self ):
		noDups = collections.OrderedDict()
		for property in timemachine.filter( self.properties.all() ):
			noDups[ property.name ] = property
		return [ p for p in noDups.values() ]

	def getPropertyValue( self, name, default ):
		properties = timemachine.filter( Property.objects.filter( ticket = self, name = name ) )
		if len( properties ) == 0:
			return default
		else:
			return properties[ : ][ -1 ].value

	def relations( self, relationName ):
		relations = timemachine.filter( Relation.objects.filter( ticket = self, name__endswith = relationName ) )
		result = collections.OrderedDict()
		for relation in relations:
			if relation.name == relationName:
				result[ relation.relatedTo.id ] = relation;
			else:
				assert relation.name == "Not " + relationName
				try:
					del result[ relation.relatedTo.id ]
				except:
					pass
		return sorted( result.values(), key = lambda x: x.order )

	def relatedByRelations( self, relationName ):
		relations = timemachine.filter( Relation.objects.filter( relatedTo = self, name__endswith = relationName ) )
		result = collections.OrderedDict()
		for relation in relations:
			if relation.name == relationName:
				result[ relation.ticket.id ] = relation;
			else:
				assert relation.name == "Not " + relationName
				try:
					del result[ relation.ticket.id ]
				except:
					pass
		return result.values()

	def childrenRelations( self ):
		return self.relations( 'Parent Of' )

	def children( self ):
		return [ r.relatedTo for r in self.childrenRelations() ]

	def parentsRelations( self ):
		return self.relatedByRelations( 'Parent Of' )

	def parents( self ):
		return [ r.ticket for r in self.parentsRelations() ]

	@timemachine.decorators.ExceptionWhileInTimeTravel()
	def addRelationAtEnd( self, name, other, user ):
		previous = self.relations( name )
		if len( previous ) == 0:
			order = 1
		else:
			order = max( p.order for p in previous ) + 1
		self.addRelation( name, other, order, user )

	@timemachine.decorators.ExceptionWhileInTimeTravel()
	def addRelation( self, name, other, order, user ):
		relation = Relation( ticket = self, relatedTo = other, name = name, user = user, order = order )
		relation.save()
		return relation

class Property( models.Model ):
	ticket = models.ForeignKey( Ticket, related_name = 'properties' )
	name = models.CharField( max_length = 200, validators = [ validateWord ] )
	value = models.CharField( max_length = 2048, validators = [ validateWord ] )
	user = models.ForeignKey( User )
	when = models.DateTimeField( auto_now = True )

	def __unicode__( self ):
		return "<Property %s>" % self.name

class Relation( models.Model ):
	ticket = models.ForeignKey( Ticket, related_name = 'relationsTo' )
	name = models.CharField( max_length = 200, validators = [ validateWord ] )
	relatedTo = models.ForeignKey( Ticket, related_name = 'relationsBy' )
	order = models.FloatField()
	user = models.ForeignKey( User )
	when = models.DateTimeField( auto_now = True )
