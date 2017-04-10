from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.expressions import RawSQL
from tourneyBrag.models import *
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid, json, random
from tourneyBrag.serializers import *

def index(request):
        return HttpResponse("Hello world and all those who inhabit it!")


class PlayerPage(APIView):
    def get(self, request, *args, **kwargs):
        playerID = request.META['QUERY_STRING']
        p = Player.objects.get(playerName = playerID)
        e = Entrant.objects.filter(
                player_entrant = playerID,
                has_been_accepted = True
                ).values('tournament_entered')
        f = Fan.objects.filter(user_Idol = playerID).values('user_Fan')
        c = Comment.objects.filter(receiver_name = playerID).values('author_name', 'actual_comment')
        player = {
                'username': p.playerName,
                #'accountType': p.acctType,
                'gamePlays': [{'gameName': p.gamePlayed}],
                #'location': p.loc,
                #'wins': p.playerWins,
                #'losses': p.playerLosses,
                'tourneysPlayed': [entry for entry in e],
                'fans': [entry for entry in f],
                'comments': [entry for entry in c],
                }
        return JsonResponse(player)


class OrganizerPage(APIView):
    def get(self, request, *args, **kwargs):
        organizerID = request.META['QUERY_STRING']
        tourneyList = []
        o = Organizer.objects.get(organizerName = organizerID)
        v = Voucher.objects.filter(
                user_receiver = organizerID
                ).values('user_voucher')
        t = Tournament.objects.filter(organizerOwner = organizerID)
        c = Comment.objects.filter(receiver_name = organizerID).values('author_name', 'actual_comment')
        for tourney in [entry for entry in t]:
            tourneyList.append({'tournament_name': tourney.tournamentTitle})
        organizer = {
                'username': o.organizerName,
                'vouchers': [entry for entry in v],
                'tournaments': tourneyList,
                'comments': [entry for entry in c],
                }
        return JsonResponse(organizer)


class TournamentPage(APIView):
    def get(self, request, *args, **kwargs):
        tourneyID = request.META['QUERY_STRING']
        t = Tournament.objects.get(tournamentTitle = tourneyID)
        c = Comment.objects.filter(receiver_name = tourneyID).values('author_name', 'actual_comment')
        e = Entrant.objects.filter(
                tournament_entered = t,
                has_been_accepted = True).values('player_entrant')
        tourney = {
                'name': t.tournamentTitle,
                'organizer': t.organizerOwner,
                'date': t.date_start,
                'participants': [entry for entry in e],
                'comments': [entry for entry in c],
                }
        return JsonResponse(tourney)


#Lists all players
class PlayerList(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 generics.GenericAPIView):
        queryset = Player.objects.all()
        serializer_class = PlayerSerializer

        def get(self, request, *args, **kwargs):
                return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
                num = random.randint(0, 2147483647)
                while Player.objects.filter(playerID=num):
                                        num = random.randint(0, 2147483647)
                request.data['playerID'] = num
                return self.create(request, *args, **kwargs)

#       def get(self, request):
                #players = Player.objects.all()
                #serializer = PlayerSerializer(players, many=True)
                #return Response(serializer.data)

        #def post(self, request):
#               num = random.randint(0, 2147483647)
                #while Player.objects.filter(Player__playerID=num):
#                       num = random.randint(0, 2147483647)
                #serializer = PlayerSerializer(data=request.data)
                #serializer.data['playerID'] = num
                #if serializer.is_valid():
#                       serializer.save()
                        #return Response(serializer.data, status=status.HTTP_201_CREATED)
                #newPlayer = Player(num, request.Post['playerName'], request.Post['password'], request.Post['gamePlayed'], request.Post['mainCharacter'])
                #newPlayer.save()
                #return Response("New player has been added!")


#Lists all organizerss
class OrganizerList(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 generics.GenericAPIView):
        queryset = Organizer.objects.all()
        serializer_class = OrganizerSerializer

        def get(self, request, *args, **kwargs):
                return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
                num = random.randint(0, 2147483647)
                while Player.objects.filter(playerID=num):
                                        num = random.randint(0, 2147483647)
                request.data['playerID'] = num
                return self.create(request, *args, **kwargs)


#Lists all tournamnts
class TournamentsList(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 generics.GenericAPIView):
        queryset = Tournament.objects.all()
        serializer_class = TournamentSerializer

        def get(self, request, *args, **kwargs):
                return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
                return self.create(request, *args, **kwargs)

#Lists all tournamnts for a specific organizer
class TournamentsSpecificList(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 generics.GenericAPIView):
        queryset = Tournament.objects.all()
        serializer_class = TournamentSerializer

        def get(self, request, *args, **kwargs):
                organizr = request.data('organizerOwner')
                queryset = Tournament.objects.all()#filter(organizerOwner = organizr)
                allSet = TournamentSerializer(queryset, many=True)
                print(allSet)
                return Response(allSet.data)

        def post(self, request, *args, **kwargs):
                num = random.randint(0, 2147483647)
                while Player.objects.filter(playerID=num):
                                        num = random.randint(0, 2147483647)
                request.data['playerID'] = num
                return self.create(request, *args, **kwargs)


#def Register(request):
#    # Query for existing username and email, insert into database, reply with affirm
#    return None
#
#def Login(request):
#    # Query for username + pass, compare hashed pass with onsite pass, reply
#    # with affirm
#    return None
#
#def CreateTournament(request):
#    # Query for existing tourney name, insert into database, reply with affirm
#    return None
#
#def ModifyTournament(request):
#    # Update tourney values in database, reply with affirm
#    return None
#
#def Comment(request):
#    # Insert comment values into database, reply with affirm
#    return None
#
#def Application(request):
#    # Modify tourney, player, organizer for type of application management,
#    # reply with affirm
#    return None
#
#def Ban(request):
#    # Modify profile of given username with appropriate values, reply with
#    # affirm
#    return None
#
#def BecomeFan(request):
#    # Modify profiles of given usernames with appropriate values, reply with
#    # affirm
#    return None
#
#def BecomeVoucher(request):
#    # Modify profiles of given usernames with appropriate values, reply with
#    # affirm
#    return None
#
#def ModifyProfile(request):
#    # Update profile values in database, reply with affirm
#    return None
#
#def Logout(request):
#    # required?
#    return None
#
