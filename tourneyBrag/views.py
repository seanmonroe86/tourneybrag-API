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
                        ban = {'date': '0000-00-00', 'reason': u.acctType}
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
        try:
            b = Banned.objects.get(user = playerID)
            isBanned = True
        except Banned.DoesNotExist:
            isBanned = False
        e = Entrant.objects.filter(
                name = playerID,
                has_been_accepted = True
                ).values('tournament_entered')
        f = Fan.objects.filter(user_Idol = playerID).values('user_Fan')
        c = Comment.objects.filter(
                receiver_name = playerID
                ).values('author_name', 'actual_comment')
        g = GamePlayed.objects.filter(
                player = playerID
                ).values('game', 'character')
        r = Reported.objects.filter(target = playerID).values('actor')
        reported = []
        for tar in r:
            reported.append(tar['actor'])
        player = {
                'username': p.username,
                'acctType': p.acctType,
                'gamePlays': [entry for entry in g],
                'description': p.description,
                'location': p.loc,
                'wins': p.playerWins,
                'losses': (p.playerGames - p.playerWins),
                'tourneysPlayed': [entry for entry in e],
                'fans': [entry for entry in f],
                'comments': [entry for entry in c],
                'banflags': p.banFlag,
                'reported': reported,
                'banned': isBanned,
                }
        return JsonResponse(player)

    def post(self, request, *args, **kwargs):
        p = json.loads(request.body)

        try:
            thePlayer = Player.objects.get(username = p['username'])
            thePlayer.loc = p['location']
            thePlayer.description = p['description']
            thePlayer.save()
            return HttpResponse("Player Updated", status = 202)
        except Player.DoesNotExist:
            try:
                if p['editing']: pass
                player = Player(
                        username = p['username'],
                        loc = p['location'],
                        description=p['description']
                        )
    
            except KeyError:
                player = Player(
                        username = p['username'],
                        password = p['password'],
                        loc = p['location'],
                        description=p['description']
                        )
            try:
                player.save()
                return HttpResponse("Player created", status = 201)
            except:
                return HttpResponse("Error creating player", status = 405)
        except:
            return HttpResponse("Error saving player to database", status = 405)


class OrganizerPage(APIView):
    def get(self, request, *args, **kwargs):
        organizerID = request.META['QUERY_STRING']
        tourneyList = []
        try:
            o = Organizer.objects.get(username = organizerID)
        except Organizer.DoesNotExist:
            return JsonResponse({'name': 'DNE'})
        try:
            b = Banned.objects.get(user = organizerID)
            isBanned = True
        except Banned.DoesNotExist:
            isBanned = False
        v = Voucher.objects.filter(
                user_receiver = organizerID
                ).values('user_voucher')
        t = Tournament.objects.filter(organizerOwner = organizerID)
        c = Comment.objects.filter(
                receiver_name = organizerID
                ).values('author_name', 'actual_comment')
        r = Reported.objects.filter(target = organizerID).values('actor')
        for tourney in [entry for entry in t]:
            tourneyList.append({'tournament_name': tourney.tournamentTitle})
        reported = []
        for tar in r:
            reported.append(tar['actor'])
        organizer = {
                'username': o.username,
                'acctType': o.acctType,
                'vouchers': [entry for entry in v],
                'tournaments': tourneyList,
                'location': o.loc,
                'comments': [entry for entry in c],
                'description': o.description,
                'banflags': o.banFlag,
                'reported': reported,
                'banned': isBanned,
                }
        return JsonResponse(organizer)

    def post(self, request, *args, **kwargs):
        o = json.loads(request.body)
        try:
            organizer = Organizer.objects.get(username = o['username'])
            organizer.loc = o['location']
            organizer.description = o['description']
        except Organizer.DoesNotExist:
            organizer = Organizer(
                    username = o['username'],
                    password = o['password'],
                    loc = o['location'],
                    description = o['description'],
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
        try:
            t = Tournament.objects.get(tournamentTitle = tourneyName)
        except Tournament.DoesNotExist:
            return JsonResponse({'name': 'DNE'})
        try:
            b = Banned.objects.get(user = tourneyName)
            isBanned = True
        except Banned.DoesNotExist:
            isBanned = False
        c = Comment.objects.filter(receiver_name = tourneyName).values('author_name', 'actual_comment')
        e = Entrant.objects.filter(
                tournament_entered = tourneyName,
                has_been_accepted = True
                ).values('name')  #players who applied and have been accepted
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
        r = Reported.objects.filter(target = tourneyName).values('actor')
        matchList = []
        for aMatch in m:
            matchList.append({"playerA": aMatch.playerA, "playerB": aMatch.playerB})
        reported = []
        for tar in r:
            reported.append(tar['actor'])

        tourney = {
                'name': t.tournamentTitle,
                'organizer': t.organizerOwner,
                'date': t.date_start,
                'participants': [entry for entry in e],
                'applicants': [applicant for applicant in a],
                'denied': [entry for entry in d],
                'matches': matchList,
                'comments': [entry for entry in c],
                'status': t.status,
                'banflags': t.banFlag,
                'reported': reported,
                'banned': isBanned,
                }
        return JsonResponse(tourney)

    def post(self, request, *args, **kwargs):
        t = json.loads(request.body)
        tourney = Tournament(
                organizerOwner = t['organizer'],
                tournamentTitle = t['name'],
                date_start = t['date'],
                status = t['status']
                )
        try:
            tourney.save()
            return HttpResponse("Tournament created", status = 201)
        except:
            return HttpResponse("Error creating tournament", status = 405)


class AddGame(APIView):
    def post(self, request, *args, **kwargs):
        g = json.loads(request.body)
        try:
            game = GamePlayed.objects.get(
                    player = g['player'],
                    game = g['game'],
                    character = g['character'])
            return HttpResponse("Duplicate entry", status = 409)
        except GamePlayed.DoesNotExist:
            game = GamePlayed(
                    player = g['player'],
                    game = g['game'],
                    character = g['character']
                    )
        try:
            game.save()
            return HttpResponse("Game added", status = 201)
        except:
            return HttpResponse("Error adding game", status = 405)


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
    def post(self, request, *args, **kwargs):   #is this supposed to be get?
        terms = json.loads(request.body)
        n, o, d, s = terms["name"], terms["organizer"], terms["date"], terms["status"]
        if n == "": tourneys = Tournament.objects.all().values(
                "tournamentTitle", "organizerOwner", "date_start"
                )
        else: tourneys = Tournament.objects.filter(tournamentTitle = n).values(
                "tournamentTitle", "organizerOwner", "date_start"
                )
        if o != "": tourneys = tourneys.filter(organizerOwner = o)
        if d != "": tourneys = tourneys.filter(date_start = d)
        if s != "": tourneys = tourneys.filter(status = s)
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
        req = json.loads(request.body)
        denied = req['denied']
        try:
            e = Entrant.objects.get(
                    name = req['name'],
                    tournament_entered = req['tournament_entered']
                    )
        except Entrant.DoesNotExist:
            return HttpResponse("Applicant {} not found".format(req['name']), status = 404)
        if not denied: e.has_been_accepted = True
        else: e.has_been_denied = True
        try:
            e.save()
        except:
            return HttpResponse("Error saving applicant", status = 405)
        return HttpResponse("Applicant processed", status = 200)


class ApplicationSign(APIView):
    def post(self, request, *args, **kwargs):
        app = json.loads(request.body)
        specificTouney = app['tournament_entered']
        player = app['name']
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
        fan = json.loads(request.body)
        newFan = fan['user_Fan']
        theIdol = fan['user_Idol']
        newFanObj = Fan(user_Fan = newFan, user_Idol = theIdol)
        try:
            newFanObj.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MakeVoucher(APIView):
    def post(self, request, *args, **kwargs):
        vouch = json.loads(request.body)
        newVoucher = vouch['user_voucher']
        theReceiver = vouch['user_receiver']
        newVoucherObj = Voucher(
                user_voucher = newVoucher,
                user_receiver = theReceiver
                )
        try:
            newVoucherObj.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReportThem(APIView):
    def post(self, request, *args, **kwargs):
        report = json.loads(request.body)
        reporter = hammer['actor']
        reportee = hammer['target']
        newReportedUser = Reported(
                actor = reporter,
                target = reportee,
                )
        try:
            newReportedUser.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BanThem(APIView):
    def post(self, request, *args, **kwargs):
        hammer = json.loads(request.body)
        actingAdmin = hammer['admin']
        userThatIsBanned = hammer['bannedUser']
        timeBanned = hammer['bannedUntil']
        reasonForBan = hammer['reason']
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
        match = json.loads(request.body)
        tourneyTitle = match['tournamentTitle']
        plyrA = match['playerA']
        plyrB = match['playerB']
        theWinner = ""   #If update is implemented, then check for winner string

        try:
            theMatch = Match.objects.get(
                tournamentTitle=tourneyTitle,
                playerA=plyrA,
                playerB=plyrB
            )
            #theMatch.winner = theWinner
            #try:
            #    theMatch.save(update_fields = ['winner'], force_update = True)
            #    return Response(status = status.HTTP_202_ACCEPTED)
            #except:
            return Response(status=status.HTTP_409_CONFLICT)
        except Match.DoesNotExist:
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
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

