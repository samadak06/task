from rest_framework import serializers


# posts/serializers.py
from rest_framework import serializers
from . import models


class LuggageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'price', 'status')
        model = models.LuggageType


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'items', 'booked_by', 'total_price')
        read_only_fields = ['total_price','booked_by']
        model = models.Booking


class userProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.userProfile
        fields = ('username', 'email', 'password',)
        read_only_fields = ['user_type', 'user','maximum_booking']