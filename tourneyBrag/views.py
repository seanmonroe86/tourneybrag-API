from django.http import HttpResponse, JsonResponse
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from tourneyBrag.models import *
from tourneyBrag.serializers import *
import json


class Login(APIView):
    def post(self, request, *args, **kwargs):
        user = json.loads(request.body)
        userID = user['username']
        userPass = user['password']
        objs = [Player, Organizer, Administrator]
        for Type in objs:
            try:
                u = Type.objects.get(username = userID)
                if u.password == userPass:
                    try:
                        b = Banned.objects.get(user = userID)
                        ban = {'date': b.date,'reason': b.reason}
                    except Banned.DoesNotExist:
                        ban = {'date': 0000-00-00,'reason': ''}
                    return JsonResponse(ban)
                else:
                    r = {'date': 9999-99-99,'reason': 'Invalid password'}
                    return JsonResponse(r)
            except Type.DoesNotExist:
                pass
        r = {'date': 1234-56-78,'reason': 'User not found'}
        return JsonResponse(r)

class Register(APIView):
    def post(self, request, *args, **kwargs):
        user = json.loads(request.body)
        userID = user['username']
        userType = user['type']

        objs = [Player, Organizer, Administrator]
        for Type in objs:
            try:
                u = Type.objects.get(username = userID)
                return HttpResponse("Username {} taken".format(userID), status = 409)
            except Type.DoesNotExist:
                pass
        if userType == 'player':
            return PlayerPage.post(self, request, args, kwargs)
        elif userType == 'organizer':
            return OrganizerPage.post(self, request, args, kwargs)
        else: return HttpResponse(
        "Invalid user type \"{}\" (bad frontend!)".format(userType), status = 405)


class PlayerPage(APIView):
    def get(self, request, *args, **kwargs):
        playerID = request.META['QUERY_STRING']
        try:
            p = Player.objects.get(username = playerID)
        except Player.DoesNotExist:
            return HttpResponse("Player {} not found.".format(playerID), status = 404)
        e = Entrant.objects.filter(
                player_entrant = playerID,
                has_been_accepted = True
                ).values('tournament_entered')
        f = Fan.objects.filter(user_Idol = playerID).values('user_Fan')
        c = Comment.objects.filter(receiver_name = playerID).values('author_name', 'actual_comment')
        player = {
                'username': p.username,
                'accountType': p.accountType,
                'gamePlays': [{'gameName': p.gamePlayed}],
                'mainchar': p.mainCharacter,
                'location': p.loc,
                'wins': p.playerWins,
                'losses': (p.playerGames - p.playerWins),
                'tourneysPlayed': [entry for entry in e],
                'fans': [entry for entry in f],
                'comments': [entry for entry in c],
                }
        return JsonResponse(player)

    def post(self, request, *args, **kwargs):
        p = json.loads(request.body)
        player = Player(
                username = p['username'],
                password = p['password'],
                gamePlayed = p['gamePlays'],
                mainCharacter = p['mainchar'],
                )
        player.save()
        return HttpResponse("Player created", status = 201)


class OrganizerPage(APIView):
    def get(self, request, *args, **kwargs):
        organizerID = request.META['QUERY_STRING']
        tourneyList = []
        o = Organizer.objects.get(username = organizerID)
        v = Voucher.objects.filter(
                user_receiver = organizerID
                ).values('user_voucher')
        t = Tournament.objects.filter(organizerOwner = organizerID)
        c = Comment.objects.filter(receiver_name = organizerID).values('author_name', 'actual_comment')
        for tourney in [entry for entry in t]:
            tourneyList.append({'tournament_name': tourney.tournamentTitle})
        organizer = {
                'username': o.username,
                'vouchers': [entry for entry in v],
                'tournaments': tourneyList,
                'comments': [entry for entry in c],
                }
        return JsonResponse(organizer)

    def post(self, request, *args, **kwargs):
        o = json.loads(request.body)
        organizer = Organizer(
                username = o['username'],
                password = o['password'],
                )
        organizer.save()
        return HttpResponse("Organizer created", status = 201)


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

    def post(self, request, *args, **kwargs):
        t = json.loads(request.body)
        tourney = Tournament(
                organizerOwner = t['organizer'],
                tournamentTitle = t['name'],
                date_start = t['date']
                )
        tourney.save()
        return HttpResponse("Tournament created", status = 201)


class MakeComment(APIView):
    def post(self, request, *args, **kwargs):
        c = json.loads(request.body)
        comment = Comment(
                author_name = c['author'],
                receiver_name = c['receiver'],
                actual_comment = c['comment']
                )
        comment.save()
        return HttpResponse("Comment posted", status = 201)


#Lists all players
class PlayerList(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 generics.GenericAPIView):
        queryset = Player.objects.all()
        serializer_class = PlayerSerializer

        def get(self, request, *args, **kwargs):
                return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
#                num = random.randint(0, 2147483647)
#                while Player.objects.filter(playerID=num):
#                                        num = random.randint(0, 2147483647)
#                request.data['playerID'] = num
                return self.create(request, *args, **kwargs)


#Lists all organizerss
class OrganizerList(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 generics.GenericAPIView):
        queryset = Organizer.objects.all()
        serializer_class = OrganizerSerializer

        def get(self, request, *args, **kwargs):
                return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
#                num = random.randint(0, 2147483647)
#                while Player.objects.filter(playerID=num):
#                                        num = random.randint(0, 2147483647)
#                request.data['playerID'] = num
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
#                num = random.randint(0, 2147483647)
#                while Player.objects.filter(playerID=num):
#                                        num = random.randint(0, 2147483647)
#                request.data['playerID'] = num
                return self.create(request, *args, **kwargs)


#def CreateTournament(request):
#    # Query for existing tourney name, insert into database, reply with affirm
#    return None
#
#def ModifyTournament(request):
#    # Update tourney values in database, reply with affirm
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
