from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.generic import ListView
from .models import Ride_Event, Ride, User
from .utils.geo import haversine
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Case, When
from .serializer import Ride_Serializer
from .utils.populate_db import populate_rider_db, populate_events, populate_user

debug = True

# Create your views here.
class Ride_Listview(ListView):
    required_role = 'admin'
    template_name = "Ride_List/ridelist.html"
    #model = Ride
    context_object_name = "ridelist"
    paginate_by = 20
    
    #catch login role before continuing
    def dispatch(self, request, *args, **kwargs):
        session_role = request.session.get('role')
        #print ("session role ", session_role)
        if not session_role and session_role != 'admin':
            #print ("valid user")
            return redirect('login-page')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Ride.objects.select_related('id_rider', 'id_driver')

        #ride status filter
        ride_status_query = self.request.GET.get('ride_status')

        if ride_status_query != None and ride_status_query.lower() in ['available', 'pickup', 'drop-off', 'reserved', 'cancelled']:
            queryset = queryset.filter(status=ride_status_query)
            #print ("status query : ", queryset)
           
        #rider email filter
        rider_email_query = self.request.GET.get('rider_email')
        if rider_email_query:
            queryset = queryset.filter(id_rider__email=rider_email_query)
            print ("rider email query : ", rider_email_query)
            
        #sorting by pickup time
        sort_by_pickuptime = self.request.GET.get('sort', 'id_ride')
        if sort_by_pickuptime in ['pickup_time', '-pickup_time']: 
            #print ("pickup", sort_by_pickuptime)
            queryset = queryset.order_by(sort_by_pickuptime)
            #print ("What's in the queryset : ", queryset.values_list('pickup_longitude', 'pickup_latitude'))

        #filtering by today's rides
        today_query = self.request.GET.get('today')
        if today_query == 'true':
            start_of_today = now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_today = start_of_today + timedelta(hours=24)
            queryset = queryset.filter(pickup_time__gte=start_of_today, pickup_time__lt=end_of_today)
            #print("Filtering for today's rides:", start_of_today, "to", end_of_today)
        
        #sort by distance
        longitude = self.request.GET.get('Longitude')
        latitude = self.request.GET.get('Latitude')
        if longitude and latitude:

            longitude = float(longitude)
            latitude = float(latitude)
            distance_list = []

            pickup_points = queryset.values('id_ride', 'pickup_longitude', 'pickup_latitude')
            for pickup_point in pickup_points:
                distance = haversine(
                    longitude, 
                    latitude, 
                    pickup_point['pickup_longitude'], 
                    pickup_point['pickup_latitude']
                    )
                distance_list.append((pickup_point['id_ride'], distance))
            
            # Sort by distance
            distance_list.sort(key=lambda x: x[1])  # Sort by the distance value
            #print (distance_list)
            
            # Extract sorted ride IDs
            sorted_ride_ids = [ride_id for ride_id, dist in distance_list]
            #print ("sorted" , sorted_ride_ids)
            
            # Create a mapping of ride ID to its index in the sorted list
            id_to_index = {ride_id: index for index, ride_id in enumerate(sorted_ride_ids)}
            #print ("index", id_to_index)

            # Sort the original queryset based on the sorted ride IDs basically creating an sql CASE and WHEN statement
            preserved_order = Case(
                *[When(id_ride=ride_id, then=pos) for pos, ride_id in enumerate(sorted_ride_ids)]
            )
            #print("preserved order", preserved_order)
            queryset = queryset.filter(id_ride__in=sorted_ride_ids).order_by(preserved_order)

        return queryset

    #cleaning the status dropdown to show only unique statuses
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_statuses = Ride.objects.values_list('status', flat=True).distinct()
        context['unique_statuses'] = unique_statuses
        #print ("unique statuses:", unique_statuses)
        return context

    

def index(request):
    return HttpResponse("Hello, world. You're at the Ride_List index.") 

def login(request):
    if request.method == 'POST':
        firstname = request.POST.get('fname')  # This matches the input name
        lastname = request.POST.get('lname')
        print("Login request received from:", firstname, lastname)

        # Now you can query your custom Users table
        try:
            user = User.objects.get(first_name=firstname, last_name=lastname)
            request.session['role'] = user.role
            print ("user ", user)
            print (user.role)
            if user.role == 'admin':
                return redirect('ridelist-page')  # Or role-based redirect
            else:
                return redirect('login-page')
        except User.DoesNotExist:
            return redirect('login-page')

    return render(request, 'Ride_List/login.html')


def populate_db(request):
    populate_rider_db()
    populate_events()
    populate_user()
    return HttpResponse("Database populated with sample data.")


      