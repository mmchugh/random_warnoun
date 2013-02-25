from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'selections.views.index', name='index'),
    url(r'^players$', 'selections.views.view_players', name='players'),
    url(r'^casters$', 'selections.views.view_casters', name='casters'),
    url(r'^create_tournament$', 'selections.views.create_tournament', name='create-tournament'),
    url(r'^add_round$', 'selections.views.add_tournament_round', name='add-round'),
    url(r'^rounds$', 'selections.views.tournament_rounds', name='view-rounds'),
    url(r'^rounds/(?P<round_number>[0-9]+)$', 'selections.views.printable_round', name='view-round'),

    url(r'^admin/', include(admin.site.urls)),
)
