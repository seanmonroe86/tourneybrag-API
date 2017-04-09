from rest_framework import serializers
from tourneyBrag.models import *

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'

#class OrganizerProfileSerializer(serializers.Serializer):


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fan
        fields = '__all__'


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'


class EntrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrant
        fields = '__all__'



class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class BannedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banned
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

