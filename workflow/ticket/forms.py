from django import forms
from workflow.customworkflow import customworkflow 

class NewTicket( forms.Form ):
	title = forms.CharField( required = True )
	state = forms.ChoiceField( choices = [ ( x.name, x.name ) for x in customworkflow.ALL_STATES if x.showAsNew ], required = True )

class SetProperty( forms.Form ):
	ticket = forms.DecimalField( widget = forms.HiddenInput(), required = True )
	property = forms.CharField( widget = forms.TextInput( attrs = { 'readonly': 'readonly' } ), required = True )
	value = forms.CharField( widget = forms.Textarea, required = True )

class SetStateProperty( forms.Form ):
	ticket = forms.DecimalField( widget = forms.HiddenInput(), required = True )
	property = forms.CharField( widget = forms.TextInput( attrs = { 'readonly': 'readonly' } ), required = True )
	value = forms.ChoiceField( choices = [ ( x.name, x.name ) for x in customworkflow.ALL_STATES ], required = True )

class SpawnChild( forms.Form ):
	ticket = forms.DecimalField( widget = forms.HiddenInput(), required = True )
	state = forms.CharField( widget = forms.TextInput( attrs = { 'readonly': 'readonly' } ), required = True )
	title = forms.CharField( required = True )
