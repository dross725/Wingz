from faker import Faker
from .models import Ride, User, Ride_Event
import random
from django.utils.timezone import now

def populate_rider_db():
    rider = list(User.objects.filter(role='Rider'))
    driver = list(User.objects.filter(role='Driver'))

    for _ in range(50):
        fake = Faker()

        status = random.choice(['Pickup', 'Drop-off', 'Reserved', 'Cancelled'])
        id_rider = random.choice(rider)
        id_driver = random.choice(driver)
        pickup_latitude = fake.latitude()
        pickup_longitude = fake.longitude()
        dropoff_latitude = fake.latitude()
        dropoff_longitude = fake.longitude()
        pickup_time = fake.date_time_this_year(before_now=True, after_now=False, tzinfo =None)

        ride = Ride(
            status=status,
            id_rider=id_rider,
            id_driver=id_driver,
            pickup_latitude=pickup_latitude,
            pickup_longitude=pickup_longitude,
            dropoff_latitude=dropoff_latitude,
            dropoff_longitude=dropoff_longitude,
            pickup_time=pickup_time
        )
        ride.save() 
        print(f"Ride created: {ride}")

def populate_events():

    rides = list(Ride.objects.all())
    descriptions = [
        "Rider requested a ride.",
        "Driver assigned to the ride.",
        "Driver is on the way to pick up the rider.",
        "Rider has been picked up.",
        "Rider has been dropped off at the destination.",
        "Ride has been cancelled by the rider.",
        "Ride has been cancelled by the driver."
    ]

    for ride in rides:
        fake = Faker()
        num_events = random.randint(1, 5)
        event_times = sorted([fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None) for _ in range(num_events)])

        for event_time in event_times:
            description = random.choice(descriptions)
            ride_event = Ride_Event(
                id_ride=ride,
                description=description,
                created_at=event_time
            )
            ride_event.save()
            print(f"Event created for Ride {ride.id_ride}: {ride_event}")