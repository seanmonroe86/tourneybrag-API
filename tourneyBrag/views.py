from django.core import serializers
from django.http import HttpResponse
from django.db.models.expressions import  RawSQL
from tourneyBrag.models import *
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
import json
import random
from tourneyBrag.serializers import *

def index(request):
	return HttpResponse("Hello world and all those who inhabit it!")

class PlayerDetails(mixins.RetrieveModelMixin,
					mixins.UpdateModelMixin,
					mixins.DestroyModelMixin,
					generics.GenericAPIView):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer


	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)


	#def delete(self, request, *args, **kwargs):
	#	return self.destroy(request, *args, **kwargs)

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

#	def get(self, request):
		#players = Player.objects.all()
		#serializer = PlayerSerializer(players, many=True)
		#return Response(serializer.data)

	#def post(self, request):
#		num = random.randint(0, 2147483647)
		#while Player.objects.filter(Player__playerID=num):
#			num = random.randint(0, 2147483647)
		#serializer = PlayerSerializer(data=request.data)
		#serializer.data['playerID'] = num
		#if serializer.is_valid():
#			serializer.save()
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
	#	return self.retrieve(request, *args, **kwargs)


	#def put(self, request, *args, **kwargs):
	#	return self.update(request, *args, **kwargs)


	#def delete(self, request, *args, **kwargs):
	#	return self.destroy(request, *args, **kwargs)

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


class Register(request):
    # Query for existing username and email, insert into database, reply with affirm
    return None

class Login(request):
    # Query for username + pass, compare hashed pass with onsite pass, reply
    # with affirm
    return None

class CreateTournament(request):
    # Query for existing tourney name, insert into database, reply with affirm
    return None

class ModifyTournament(request):
    # Update tourney values in database, reply with affirm
    return None

class Comment(request):
    # Insert comment values into database, reply with affirm
    return None

class Application(request):
    # Modify tourney, player, organizer for type of application management,
    # reply with affirm
    return None

class Ban(request):
    # Modify profile of given username with appropriate values, reply with
    # affirm
    return None

class BecomeFan(request):
    # Modify profiles of given usernames with appropriate values, reply with
    # affirm
    return None

class BecomeVoucher(request):
    # Modify profiles of given usernames with appropriate values, reply with
    # affirm
    return None

class ModifyProfile(request):
    # Update profile values in database, reply with affirm
    return None

class Logout(request):
    # required?
    return None

class TournamentPage(request):
    # Query for everything on tourney page of given name, reply with JSON
    # string


