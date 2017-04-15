from django.http import HttpResponse, JsonResponse
from rest_framework import generics, mixins, status
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
        tourneyName = request.META['QUERY_STRING']
        t = Tournament.objects.get(tournamentTitle = tourneyName)
        c = Comment.objects.filter(receiver_name = tourneyName).values('author_name', 'actual_comment')
        e = Entrant.objects.filter(
                tournament_entered = t,
                has_been_accepted = True).values('player_entrant')
        a = Entrant.objects.filter(tournament_entered = tourneyName, has_been_accepted=False).values('player_entrant')  #players who applied but not been accepted
        m = Match.objects.filter(tournamentTitle=tourneyName)

        matchList = []

        for aMatch in m:
            matchList.append({aMatch.playerA, aMatch.playerB})

        tourney = {
                'name': t.tournamentTitle,
                'organizer': t.organizerOwner,
                'date': t.date_start,
                'participants': [entry for entry in e],
                'applicants': [applicant for applicant in a],
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
class PlayerList(APIView):

        def get(self, request, *args, **kwargs):
            allPlayers = Player.objects.all()


            playerList = []

            for player in allPlayers:
                playerList.append({'username': player.username,
                                    'gamePlayed': player.tournamentTitle,
                                    'mainCharacter': player.date_created,
                                    'accountType': player.date_start,
                                    'location': player.loc})

            return JsonResponse(playerList, status=status.HTTP_200_OK)

        def post(self, request, *args, **kwargs): #This is not to
            username = Player.objects.get(username = request.data['username'])

            if username:
                return Response("Player Already Exists.", status=status.HTTP_409_CONFLICT)
            else:
                new_username = request.data['username']
                new_password = request.data['password']
                new_gamePlayed = request.data['gamePlayed']
                new_mainCharacter = request.data['mainCharacter']
                new_loc = request.data['loc']

                newPlayer = Player(username=new_username,
                                   password=new_password,
                                   gamePlayed=new_gamePlayed,
                                   mainCharacter=new_mainCharacter,
                                   accountType="player",
                                   loc=new_loc)

                newPlayer.save()
                return Response(status=status.HTTP_201_CREATED)



#Lists all organizerss
class OrganizerList(APIView):

        def get(self, request, *args, **kwargs):
            allOrganizers = Organizer.objects.all()

            organizerList = [theOrganizer.username for theOrganizer in allOrganizers]

            return JsonResponse(organizerList, status=status.HTTP_200_OK)

        #Doesn't need post since OrganizerPage does it


#Lists all tournamnts
class TournamentsList(APIView):

        def get(self, request, *args, **kwargs):
            allTourneys = Tournament.objects.all()

            tourneyList = []

            for tournament in allTourneys:
                tourneyList.append({'organizerOwner':tournament.organizerOwner,
                                    'tournamentTitle': tournament.tournamentTitle,
                                    'date_created': tournament.date_created,
                                    'date_start': tournament.date_start})


            return JsonResponse(tourneyList, status=status.HTTP_200_OK)

        def post(self, request, *args, **kwargs):               #change this
                return self.create(request, *args, **kwargs)

#Lists all tournamnts for a specific organizer
#class TournamentsSpecificList(APIView):           #Commented off since its not needed due to the fact that OrganizerPage does this

        #def get(self, request, *args, **kwargs):
#                organizr = request.data('organizerOwner')
#                queryset = Tournament.objects.all()#filter(organizerOwner = organizr)
#                allSet = TournamentSerializer(queryset, many=True)
#                #print(allSet)
#                return Response(allSet.data)

#        def post(self, request, *args, **kwargs):
#                num = random.randint(0, 2147483647)
#                while Player.objects.filter(playerID=num):
#                                        num = random.randint(0, 2147483647)
#                request.data['playerID'] = num
#                return self.create(request, *args, **kwargs)

class ApplicationList(APIView):
    def get(self, request, *args, **kwargs):
        organizerName = request.META['QUERY_STRING']
        theOrganizer = Organizer.objects.get(username = organizerName)
        allTournaments = Tournament.objects.filter(organizerOwner = theOrganizer).values('tournamentTitle')
        allEntrants = Entrant.objects.filter(tournament_entered__in = allTournaments, has_been_accepted=False).values('tournament_entered', 'player_entrant')

        entrantsList = []

        for entrant in allEntrants:
            entrantsList.append({
            'theTournament': entrant.tournament_entered,
            'entrant': entrant.player_entrant})
        return JsonResponse(entrantsList, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        specificTouney = request.data['tournament_entered']
        player = request.data['player_entrant']
        newEntrant = Entrant(player_entrant = player, tournament_entered = specificTouney, has_been_accepted = False)
        newEntrant.save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pass



class FanList(APIView):
    #No get because this will be done in player profile
   # def get(self, request, *args, **kwargs):
    #    fanList = Fan.objects.filter(idolID = self.kwargs['pk'])
     #   return JsonResponse(fanList, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        newFan = request.data['user_Fan']
        theIdol = request.data['user_Idol']
        #idolsID = request.data['idolID']
        newFanObj = Fan(user_Fan = newFan, user_Idol = theIdol)
        newFanObj.save()
        return Response(status=status.HTTP_201_CREATED)

class VoucherList(APIView):
    # No get because this will be done in organizer profile
    #def get(self, request, *args, **kwargs):
    #    voucherList = Voucher.objects.filter(user_receiver= request.META['QUERY_STRING']).values('user_voucher')#request.META['QUERY_STRING'])
    #    vouchDict = {'voucherName':[voucher for voucher in voucherList]}
    #    return JsonResponse(vouchDict, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        newVoucher = request.data['user_voucher']
        theReceiver = request.data['user_receiver']
        #receiversID = request.data['receiverID']
        newVoucherObj = Voucher(user_voucher = newVoucher, user_receiver = theReceiver)
        newVoucherObj.save()
        return Response(status=status.HTTP_201_CREATED)

#class CommentList(APIView):
#    def post(self, request, *args, **kwargs):
#        commentAuthor = request.data['author_name']
#        commentReceiver = request.data['receiver_name']
#        commentItself = request.data['actual_comment']
#        newComment = Comment(author_name = commentAuthor, receiver_name = commentReceiver, actual_comment = commentItself)
#        newComment.save()
#        return Response(status=status.HTTP_201_CREATED)

class BanHimList(APIView):
    def post(self, request, *args, **kwargs):
        actingAdmin = request.data['admin']
        userThatIsBanned = request.data['bannedUser']
        timeBanned = request.data['bannedUntil']
        reasonForBan = request.data['reason']
        newBannedUser = Banned(admin = actingAdmin, bannedUser = userThatIsBanned, bannedUntil = timeBanned, reason = reasonForBan)
        newBannedUser.save()
        return Response(status=status.HTTP_201_CREATED)

class MatchDetail(APIView): #Post = entering new match, PUT is updating
    def post(self, request, *args, **kwargs):
        tourneyTitle = request.data['tournamentTitle']
        plyrA = request.data['playerA']
        plyrB = request.data['playerB']
        theWinner = ""
        newMatch = Match(tournamentTitle = tourneyTitle, playerA = plyrA, playerB = plyrB, winner = theWinner)
        newMatch.save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        tourneyTitle = request.data['tournamentTitle']
        plyrA = request.data['playerA']
        plyrB = request.data['playerB']
        theWinner = request.data['winner']
        theMatch = Match.objects.get(tournamentTitle = tourneyTitle, playerA = plyrA, playerB = plyrB)
        if theMatch:
            theMatch.winner = theWinner
            theMatch.save(update_fields=['winner'], force_update=True)
            return Response(status = status.HTTP_202_ACCEPTED)
        else:
            Response(status= status.HTTP_422_UNPROCESSABLE_ENTITY)

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
#def Ban(request): DONE
#    # Modify profile of given username with appropriate values, reply with
#    # affirm
#    return None
#
#def BecomeFan(request): DONE
#    # Modify profiles of given usernames with appropriate values, reply with
#    # affirm
#    return None
#
#def BecomeVoucher(request): DONE
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
#
#def Modify Match: DONE
#
#
#
#
#