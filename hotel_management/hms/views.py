from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *



def booking(user, room_id, check_in_date, check_out_date):
        room = Room.objects.get(id=room_id)

        booking = Booking.objects.create(
            room=room,
            user = user,
            check_in_date=check_in_date,
            check_out_date=check_out_date
        )
        booking.save()



def our_rooms(request):
    if request.method == 'POST':
        user = request.user
        room_id = request.POST.get('room_id')
        check_in_date_string = request.session.get('check_in_date')
        check_out_date_string = request.session.get('check_out_date')

        check_in_date = datetime.strptime(check_in_date_string, '%d %B, %Y').date()
        check_out_date = datetime.strptime(check_out_date_string, '%d %B, %Y').date()

        booking(user, room_id, check_in_date, check_out_date)
        return redirect('hms:index')

    return render(request, 'main/rooms.html')


def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    # request.session['room_id'] = room_id

    # Extracting Details and Booking Room
    if request.method == "POST":
        user = request.user
        check_in_date_string = request.session.get('check_in_date')
        check_out_date_string = request.session.get('check_out_date')
        check_in_date = datetime.strptime(check_in_date_string, '%d %B, %Y').date()
        check_out_date = datetime.strptime(check_out_date_string, '%d %B, %Y').date()

        booking(user, room_id, check_in_date, check_out_date)
        return redirect('hms:index')

    return render(request, 'main/room_detail.html', {'room': room, 'room_id': room_id})


def about(request):
    return render(request, 'main/about.html')



def contact(request):
    return render(request, 'main/contact.html')




def find_available_room(room_type, check_in_date, check_out_date, beds):
    # First filters all rooms based on the room_type selected by the user

    available_rooms = Room.objects.filter(room_type=room_type, room_status='vacant')
    if beds != '0':
        available_rooms = Room.objects.filter(room_type=room_type, room_status='vacant', beds=beds)


    # filters out all the rooms that are already booked between the check_in_date and check_out_date selected by the user.
    overlapping_bookings = Booking.objects.filter(
        check_in_date__lte=check_out_date,
        check_out_date__gte=check_in_date
    )
    booked_rooms = [booking.room for booking in overlapping_bookings]
    available_rooms = available_rooms.exclude(pk__in=[room.pk for room in booked_rooms])


    return available_rooms


def index(request):
    data = {}
    if request.method == 'POST':

        checkin_string = request.POST['check_in_date']
        check_in_date = datetime.strptime(checkin_string, '%d %B, %Y').date()

        checkout_string = request.POST['check_out_date']
        check_out_date = datetime.strptime(checkout_string, '%d %B, %Y').date()

        room_type = request.POST['room_type']
        no_of_beds = request.POST.get('no_of_beds')


        if check_in_date < timezone.now().date():
            pass
            # raise forms.ValidationError("The check-in date cannot be in the past.")
        elif check_out_date < check_in_date:
            pass
            # raise forms.ValidationError("The check-out date must be after the check-in date.")

        else:
            available_rooms = find_available_room(room_type, check_in_date, check_out_date, no_of_beds)
            data['available_rooms'] = available_rooms

            request.session['check_in_date'] = checkin_string
            request.session['check_out_date'] = checkout_string

            return render(request, 'main/rooms.html', data)

    return render(request, 'main/index.html')


# AUTHORIZATION AND AUTHENTICATION
@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')


def register(request):
    register_form = None
    if request.user.is_active:
        if request.method == 'POST':
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save(commit=False)
                # verify OTP here
                # verify Email HERE
                register_form.save()
                return redirect('hms:login')
        else:
            register_form = RegisterForm()

    return render(request, 'main/register.html', {'register_form': register_form})


def login(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('hms:index')

    login_form = None
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hms:index')
            else:
                # If the user is not authenticated, add an error message to the form and render the template again
                login_form.add_error(None, 'Invalid username or password')
    else:
        login_form = LoginForm()
    return render(request, 'main/login.html', {'login_form': login_form})
