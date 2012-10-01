from workflow.ticket import models
from django.contrib import admin

admin.site.register( models.Ticket )
admin.site.register( models.Property )
admin.site.register( models.Relation )
