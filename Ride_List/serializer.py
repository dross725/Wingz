from rest_framework import serializers
from . models import *

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id_user', 
            'role', 
            'first_name', 
            'last_name',
            'email',
            'phone_number'
            ]
        
class Ride_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            'id_ride',
            'status',
            'id_rider',
            'id_driver',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time'
        ]

class Ride_Event_serializer(serializers.ModelSerializer):
    class Meta:
        model = Ride_Event
        fields = [
            'id_ride_event',
            'id_ride',
            'description',
            'created_at'
        ]