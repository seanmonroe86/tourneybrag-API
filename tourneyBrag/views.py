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
        tourney = {
                'name': t.tournamentTitle,
                'organizer': t.organizerOwner,
                'date': t.date_start,
                }
        return JsonResponse(tourney)

class PlayerDetails(APIView):#mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):



        def get(self, request, *args, **kwargs):
                return self.retrieve(request, *args, **kwargs)


        def put(self, request, *args, **kwargs):
                return self.update(request, *args, **kwargs)


        #def delete(self, request, *args, **kwargs):
        #       return self.destroy(request, *args, **kwargs)

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

                organizerVouchers = Voucher.objects.filter(user_receiver = organizer[0].organizerName).values('user_voucher')

                organizerDictionary = {'organizerName': organizer[0].organizerName,
                                        'organizerID': organizer[0].organizerID,
                                        'tournamentList': organizersTourneys,
                                        'authors_and_comments': organizersComments,
                                        'vouchers_list': [vouch for vouch in organizerVouchers]}


                #fullOrganizer = organizer#.annotate(val=RawSQL("SELECT actual_comment FROM tourneyBrag_Comments WHERE receiver_name = %s", (self.kwargs['pk'])))
                #json_data = json.dumps(allTournamentsForOrganizer)#serializers.serialize('json', fullOrganizer, many=True)
                return JsonResponse(organizerDictionary)



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

class CommentList(APIView):
    def post(self, request, *args, **kwargs):
        commentAuthor = request.data['author_name']
        commentReceiver = request.data['receiver_name']
        commentItself = request.data['actual_comment']
        newComment = Comment(author_name = commentAuthor, receiver_name = commentReceiver, actual_comment = commentItself)
        newComment.save()
        return Response(status=status.HTTP_201_CREATED)

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
        pass    

#def Register(request): DONE
#    # Query for existing username and email, insert into database, reply with affirm
#    return None
#
#def Login(request): DONE
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
#def Comment(request): DONE
#    # Insert comment values into database, reply with affirm
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
#Accepting Application
#
#
#
#
#
#
#
#
#