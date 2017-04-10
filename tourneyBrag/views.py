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

class TournamentPage(APIView):
    # Query for everything on tourney page of given name, reply with JSON
    # string
    from tourneyBrag.models import Tournament
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

class PlayerPage(APIView):
    def get(self, request, *args, **kwargs):
        playerID = request.META['QUERY_STRING']
        p = Player.objects.get(playerName = playerID)
        c = Comment.objects.filter(receiver_name = playerID).values('author_name', 'actual_comment')
        f = Fan.objects.filter(user_Idol = playerID).values('user_Fan')
        e = Entrant.objects.filter(
                player_entrant = playerID,
                has_been_accepted = True
                ).values('tournament_entered')
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


class OrganizerDetails(APIView):
        def get(self, request, *args, **kwargs):
                organizer = Organizer.objects.filter(organizerID = self.kwargs['pk'])#val=RawSQL("SELECT tournamentTitle FROM tourneyBrag_Tournament WHERE organizerOwnerID = %s", (self.kwargs['pk'])))

                allTournamentsForOrganizer = Tournament.objects.filter(organizerOwnerID = organizer[0].organizerID)

                organizersTourneys = []

                for tourneys in allTournamentsForOrganizer:
                        organizersTourneys.append(tourneys.tournamentTitle)

                Comments = Comment.objects.filter(receiver_name = organizer[0].organizerName).values('author_name', 'actual_comment')

                organizersComments = []
                for coms in Comments:
                        organizersComments.append(coms)

                organizerDictionary = {'organizerName': organizer[0].organizerName,
                                                           'organizerID': organizer[0].organizerID,
                                                           'tournamentList': organizersTourneys,
                                                           'authors_and_comments': organizersComments}


                fullOrganizer = organizer#.annotate(val=RawSQL("SELECT actual_comment FROM tourneyBrag_Comments WHERE receiver_name = %s", (self.kwargs['pk'])))
                json_data = json.dumps(allTournamentsForOrganizer)#serializers.serialize('json', fullOrganizer, many=True)
                return Response(json_data.data)



        #queryset = Organizer.objects.all()
        #serializer_class = OrganizerSerializer


        #def get(self, request, *args, **kwargs):
        #       return self.retrieve(request, *args, **kwargs)


        #def put(self, request, *args, **kwargs):
        #       return self.update(request, *args, **kwargs)


        #def delete(self, request, *args, **kwargs):
        #       return self.destroy(request, *args, **kwargs)

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
