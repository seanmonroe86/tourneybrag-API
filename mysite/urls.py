from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from tourneyBrag import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^playerpage/$', views.PlayerPage.as_view()),
    url(r'^tournamentpage/', views.TournamentPage.as_view()),
    #url(r'^ban/', views.Ban.as_view()),
    #url(r'^login/', views.Login.as_view()),
    #url(r'^logout/', views.Logout.as_view()),
    #url(r'^comment/', views.Comment.as_view()),
    #url(r'^register/', views.Register.as_view()),
    #url(r'^become-fan/', views.becomeFan.as_view()),
    #url(r'^application/', views.Application.as_view()),
    #url(r'^become-voucher/', views.BecomeVoucher.as_view()),
    #url(r'^modify-profile/', views.ModifyProfile.as_view()),
    #url(r'^create-tournament/', views.CreateTournament.as_view()),
    #url(r'^modify-tournament/', views.ModifyTournament.as_view()),
    url(r'^list-players/', views.PlayerList.as_view()),
    url(r'^list-organizers/', views.OrganizerList.as_view()),
    url(r'^list-tournaments/', views.TournamentsList.as_view()),
    url(r'^organizerprofile/(?P<pk>[0-9]+)/$', views.OrganizerDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

