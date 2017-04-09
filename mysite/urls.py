"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from tourneyBrag import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tourneys/', views.TournamentsList.as_view()),
	url(r'^playerprofiles/', views.PlayerList.as_view()),
    url(r'^organizerprofiles/', views.OrganizerList.as_view()),
    url(r'^tournaments/', views.TournamentsList.as_view()),
    #url(r'^organizerprofile/(?P<pk>[0-9]+)/$', views.TournamentsSpecificList.as_view()),
    url(r'^organizerprofile/(?P<pk>[0-9]+)/$', views.OrganizerDetails.as_view()),
    url(r'^playerprofile/(?P<pk>[0-9]+)/$', views.PlayerDetails.as_view()),
    url(r'^organizerprofile/(?P<pk>[0-9]+)/$', views.OrganizerDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)