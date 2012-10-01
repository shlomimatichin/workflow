from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'workflow.views.welcome'),
    url(r'^ticket/', include('workflow.ticket.urls')),
    url(r'^customworkflow/', include('workflow.customworkflow.urls')),
    url(r'^calendar/', include('workflow.calendar.urls')),
    url(r'^timemachine/', include('workflow.timemachine.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

	( r'^accounts/login/$', 'django.contrib.auth.views.login' ),
	( r'^accounts/logout$', 'django.contrib.auth.views.logout', { 'next_page': '/' } ),
)
