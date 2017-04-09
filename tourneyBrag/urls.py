from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from tourneyBrag import views

from . import views

urlpatterns = ['',
	url(r'^tourneys/', views.TournamentsList.as_view()),
	url(r'^profiles/', views.PlayerList.as_view()),
	]

urlpatterns = format_suffix_patterns(urlpatterns)
