from django.db import models
from django.utils.timezone import now 

# Create your models here.
class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=100, editable=True, null=False, blank=False)
    first_name = models.CharField(max_length=50, editable=True, null=False, blank=False)
    last_name = models.CharField(max_length=50, editable=True, null=False, blank=False)
    email = models.CharField(max_length=50, editable=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, editable=True, null=False, blank=False)
    def __str__(self):
        return f"{self.id_user} {self.role} {self.first_name} {self.last_name} {self.email} {self.phone_number}"
    

class Ride (models.Model):
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100, editable=True, null=False, blank=False)
    id_rider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='id_ride',
        null=True,
        blank=True
        )
    id_driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='id_driver'
    )
    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    dropoff_latitude = models.FloatField(null=True, blank=True)
    dropoff_longitude = models.FloatField(null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.id_ride} \
            {self.status} \
            {self.id_rider} \
            {self.id_driver} \
            {self.pickup_latitude} \
            {self.pickup_longitude} \
            {self.dropoff_latitude} \
            {self.dropoff_longitude} \
            {self.pickup_time} \
        "

class Ride_Event(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='ride_event'
        )
    description = models.CharField(max_length=1000, editable=True)
    created_at = models.DateTimeField(default=now)


    def __str__(self):
        return f"{self.id_ride_event} {self.id_ride} {self.description} {self.created_at}"