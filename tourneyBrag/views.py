from django.http import HttpResponse, JsonResponse
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from tourneyBrag.models import *
from tourneyBrag.serializers import *
from itertools import chain
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
                        ban = {'date': b.date, 'reason': b.reason}
                    except Banned.DoesNotExist:
                        ban = {'date': '0000-00-00', 'reason': ''}
                    return JsonResponse(ban)
                else:
                    r = {'date': '9999-99-99', 'reason': 'Invalid password'}
                    return JsonResponse(r)
            except Type.DoesNotExist:
                pass
        r = {'date': '1234-56-78', 'reason': 'User not found'}
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
                name = playerID,
                has_been_accepted = True
                ).values('tournament_entered')
        f = Fan.objects.filter(user_Idol = playerID).values('user_Fan')
        c = Comment.objects.filter(
                receiver_name = playerID
                ).values('author_name', 'actual_comment')
        player = {
                'username': p.username,
                'acctType': p.acctType,
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
        try:
            player.save()
            return HttpResponse("Player created", status = 201)
        except:
            return HttpResponse("Error creating player", status = 405)


class OrganizerPage(APIView):
    def get(self, request, *args, **kwargs):
        organizerID = request.META['QUERY_STRING']
        tourneyList = []
        o = Organizer.objects.get(username = organizerID)
        v = Voucher.objects.filter(
                user_receiver = organizerID
                ).values('user_voucher')
        t = Tournament.objects.filter(organizerOwner = organizerID)
        c = Comment.objects.filter(
                receiver_name = organizerID
                ).values('author_name', 'actual_comment')
        for tourney in [entry for entry in t]:
            tourneyList.append({'tournament_name': tourney.tournamentTitle})
        organizer = {
                'username': o.username,
                'acctType': o.acctType,
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
        try:
            organizer.save()
            return HttpResponse("Organizer created", status = 201)
        except:
            return HttpResponse("Error creating organizer", status = 405)


class AdminPage(APIView):
    def get(self, request, *args, **kwargs):
        adminID = request.META['QUERY_STRING']
        try:
            a = Administrator.objects.get(username = adminID)
        except Administrator.DoesNotExist:
            return HttpResponse("Administrator {} not found.".format(adminID), status = 404)
        b = Banned.objects.filter(
                admin = adminID
                ).values('user', 'date', 'reason')
        admin = {
                'username': a.username,
                'acctType': a.acctType,
                'has_banned': [entry for entry in b]
                }
        return JsonResponse(admin)


class TournamentPage(APIView):
    def get(self, request, *args, **kwargs):
        tourneyName = request.META['QUERY_STRING']
        t = Tournament.objects.get(tournamentTitle = tourneyName)
        c = Comment.objects.filter(receiver_name = tourneyName).values('author_name', 'actual_comment')
        e = Entrant.objects.filter(
                tournament_entered = t,
                has_been_accepted = True
                ).values('name')
        a = Entrant.objects.filter(
                tournament_entered = tourneyName,
                has_been_accepted = False,
                has_been_denied = False
                ).values('name')  #players who applied but not been accepted
        d = Entrant.objects.filter(
                tournament_entered = tourneyName,
                has_been_denied = True
                ).values('name')  #players who applied and denied
        m = Match.objects.filter(tournamentTitle=tourneyName)

        matchList = []

        for aMatch in m:
            matchList.append({"playerA": aMatch.playerA, "playerB": aMatch.playerB})

        tourney = {
                'name': t.tournamentTitle,
                'organizer': t.organizerOwner,
                'date': t.date_start,
                'participants': [entry for entry in e],
                'applicants': [applicant for applicant in a],
                'denied': [entry for entry in d],
                'matches': matchList,
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
        try:
            tourney.save()
            return HttpResponse("Tournament created", status = 201)
        except:
            return HttpResponse("Error creating tournament", status = 405)


class MakeComment(APIView):
    def post(self, request, *args, **kwargs):
        c = json.loads(request.body)
        comment = Comment(
                author_name = c['author'],
                receiver_name = c['receiver'],
                actual_comment = c['comment']
                )
        try:
            comment.save()
            return HttpResponse("Comment posted", status = 201)
        except:
            return HttpResponse("Error creating comment", status = 405)


class UsersList(APIView):
    def post(self, request, *args, **kwargs):
        terms = json.loads(request.body)
        u, t, d = terms["username"], terms["acctType"], terms["description"]
        if u == "":
            players = Player.objects.all().values(
                    "username", "description", "acctType")
            organizers = Organizer.objects.all().values(
                    "username", "description", "acctType")
        else:
            players = Player.objects.filter(username = u).values(
                    "username", "description", "acctType")
            organizers = Organizer.objects.filter(username = u).values(
                    "username", "description", "acctType")
        if d != "":
            players = players.filter(description = d)
            organizers = organizers.objects.filter(description = d)
        if t == "": users = chain(players, organizers)
        elif t == "player": users = players
        elif t == "organizer": users = organizers
        else: users = [{"username": "NULL", "description": "NULL", "type": "NULL"}]
        return JsonResponse({"users": [entry for entry in users]})


class TournamentsList(APIView):
    def post(self, request, *args, **kwargs):
        terms = json.loads(request.body)
        n, o, d = terms["name"], terms["organizer"], terms["date"]
        if n == "": tourneys = Tournament.objects.all().values(
                "tournamentTitle", "organizerOwner", "date_start"
                )
        else: tourneys = Tournament.objects.filter(tournamentTitle = n).values(
                "tournamentTitle", "organizerOwner", "date_start"
                )
        if o != "": tourneys = tourneys.filter(organizerOwner = o)
        if d != "": tourneys = tourneys.filter(date_start = d)
        return JsonResponse({"tournaments": [entry for entry in tourneys]})


class ApplicationList(APIView):
    def get(self, request, *args, **kwargs):
        organizer = request.META['QUERY_STRING']
        t = Tournament.objects.filter(
                organizerOwner = organizer
                ).values('tournamentTitle')
        tourneys = []
        for tourney in t:
            tourneys.append(tourney['tournamentTitle'])
        e = Entrant.objects.filter(
                tournament_entered__in = tourneys,
                has_been_accepted = False,
                has_been_denied = False
                ).values('name', 'tournament_entered')
        return JsonResponse({"entrants": [entry for entry in e]})

    def post(self, request, *args, **kwargs):
        denied = request.data['denied']
        e = Entrant.objects.get(
                name = request.data['name'],
                tournament_entered = request.data['tournament_entered']
                )
        if not denied: e.has_been_accepted = True
        else: e.has_been_denied = True
        e.save()
        return HttpResponse("Applicant processed", status = 200)


class ApplicationSign(APIView):
    def post(self, request, *args, **kwargs):
        specificTouney = request.data['tournament_entered']
        player = request.data['name']
        newEntrant = Entrant(
                name = player,
                tournament_entered = specificTouney,
                )
        try:
            newEntrant.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MakeFan(APIView):
    def post(self, request, *args, **kwargs):
        newFan = request.data['user_Fan']
        theIdol = request.data['user_Idol']
        newFanObj = Fan(user_Fan = newFan, user_Idol = theIdol)
        try:
            newFanObj.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MakeVoucher(APIView):
    def post(self, request, *args, **kwargs):
        newVoucher = request.data['user_voucher']
        theReceiver = request.data['user_receiver']
        newVoucherObj = Voucher(
                user_voucher = newVoucher,
                user_receiver = theReceiver
                )
        try:
            newVoucherObj.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BanThem(APIView):
    def post(self, request, *args, **kwargs):
        actingAdmin = request.data['admin']
        userThatIsBanned = request.data['bannedUser']
        timeBanned = request.data['bannedUntil']
        reasonForBan = request.data['reason']
        newBannedUser = Banned(
                admin = actingAdmin,
                user = userThatIsBanned,
                date = timeBanned,
                reason = reasonForBan
                )
        try:
            newBannedUser.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MatchDetail(APIView): #Post = entering new match, PUT is updating
    def post(self, request, *args, **kwargs):
        tourneyTitle = request.data['tournamentTitle']
        plyrA = request.data['playerA']
        plyrB = request.data['playerB']
        theWinner = ""
        newMatch = Match(
                tournamentTitle = tourneyTitle,
                playerA = plyrA,
                playerB = plyrB,
                winner = theWinner
                )
        try:
            newMatch.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        tourneyTitle = request.data['tournamentTitle']
        plyrA = request.data['playerA']
        plyrB = request.data['playerB']
        theWinner = request.data['winner']
        theMatch = Match.objects.get(
                tournamentTitle = tourneyTitle,
                playerA = plyrA,
                playerB = plyrB
                )
        if theMatch:
            theMatch.winner = theWinner
            try:
                theMatch.save(update_fields = ['winner'], force_update = True)
                return Response(status = status.HTTP_202_ACCEPTED)
            except:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            Response(status= status.HTTP_422_UNPROCESSABLE_ENTITY)

