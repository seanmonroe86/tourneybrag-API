from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from tourneyBrag import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^adminpage', views.AdminPage.as_view()),
    url(r'^playerpage', views.PlayerPage.as_view()),
    url(r'^tournamentpage', views.TournamentPage.as_view()),
    url(r'^organizerpage', views.OrganizerPage.as_view()),
    url(r'^login', views.Login.as_view()),
    url(r'^comment', views.MakeComment.as_view()),
    url(r'^register', views.Register.as_view()),
    url(r'^voucher', views.MakeVoucher.as_view()),
    url(r'^ban', views.BanThem.as_view()),
    url(r'^fan', views.MakeFan.as_view()),
    url(r'^application', views.ApplicationList.as_view()),
    url(r'^apply', views.ApplicationSign.as_view()),
    url(r'^create-match', views.MatchDetail.as_view()),
    url(r'^list-users', views.UsersList.as_view()),
    url(r'^list-tournaments', views.TournamentsList.as_view()),
    url(r'^game', views.AddGame.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

