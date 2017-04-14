from django.db import models

#If you make changes, make sure to do makemigrations and then migrate.
#If you add another table, add it to the admin.py so admins can see the table


class Player(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)
    gamePlayed = models.CharField(max_length=50)
    mainCharacter = models.CharField(max_length=30)
    accountType = models.CharField(max_length=10, default="player")
    loc = models.CharField(max_length=50)
    playerWins = models.IntegerField(default=0)
    playerGames = models.IntegerField(default=0)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.username, self.password, self.gamePlayed, self.mainCharacter)


class Organizer(models.Model):
    username = models.CharField(primary_key=True, max_length=30) # why do we have this
    password = models.CharField(max_length=30)

    def __str__(self):
        return "{}, {}".format(self.username, self.password)


class OrganizerProfile(object):
    def __init__(self, organID, organName, pw, tourneyTitle, actualComment, commentAuthor):
        self.organID = organID
        self.organName - organName
        self.pw = pw
        self.tourneyTitle = tourneyTitle
        self.actualComment = actualComment
        self.commentAuthor = commentAuthor


class Administrator(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=30)
        

class Tournament(models.Model):
    organizerOwner = models.CharField(max_length=30)
    tournamentTitle = models.CharField(max_length=30, unique= True, primary_key=True)
    date_created = models.DateTimeField('date_created', auto_now_add=True)
    date_start = models.DateTimeField('date_start')

    #def __str__(self):
    #   return self.organizerOwner + ", " + str(self.organizerOwnerID) + ", " + self.tournamentTitle + ", " + self.date_created + ", " + self.date_start


class Fan(models.Model):
    user_Fan = models.CharField(max_length=30) #user_fan is a fan of user_idol
    user_Idol = models.CharField(max_length=30)


class Voucher(models.Model):
    user_voucher = models.CharField(max_length=30) #user_voucher vouches for user_receiver
    user_receiver = models.CharField(max_length=30)


class Entrant(models.Model):
    player_entrant = models.CharField(max_length=30)
    tournament_entered = models.ForeignKey('Tournament', on_delete=models.DO_NOTHING,related_name= '+')
    has_been_accepted = models.BooleanField()


class Record(models.Model):
    tournament_name = models.ForeignKey('Tournament',on_delete=models.CASCADE,related_name= '+')
    player_winner = models.CharField(max_length=30)
    player_loser = models.CharField(max_length=30)


class Banned(models.Model):
    user = models.CharField(max_length=30)
    admin = models.CharField(max_length=30)
    date = models.DateField(default="1986-09-28")
    reason = models.CharField(max_length=50)


class Match(models.Model):
    playerA = models.CharField(max_length=30)
    playerB = models.CharField(max_length=30)
    tournamentTitle = models.CharField(max_length=30)
    winner = models.CharField(max_length=30)


class Comment(models.Model):
    author_name = models.CharField(max_length=30)
    receiver_name = models.CharField(max_length=30)
    actual_comment = models.CharField(max_length=150)
    date_created = models.DateField(auto_now_add=True)


