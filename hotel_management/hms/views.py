from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *


def index(request):
    return render(request, 'main/index.html')


def our_rooms(request):
    return render(request, 'main/rooms.html')


def room_detail(request):
    return render(request, 'main/room_detail.html')


def contact(request):
    return render(request, 'main/contact.html')


def about(request):
    return render(request, 'main/about.html')


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


# @login_required
def booking(request):

    data = {}
    show_table = False

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            user_id = request.user.id
            room_type = form.cleaned_data.get('room_type')
            bed_type = form.cleaned_data.get('bed_type')
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']

            available_rooms = find_available_room(room_type, check_in_date, check_out_date, bed_type)

            if 'show_available_room' in request.POST:
                show_table = True
                data['available_rooms'] = available_rooms

            elif 'book_now' in request.POST:
                if available_rooms:
                    available_rooms= available_rooms[0]
                    # Since Room is available to create Booking
                    room_id = available_rooms.id
                    room = Room.objects.get(id=room_id)
                    myUser = User.objects.get(id=user_id)

                    booking = Booking.objects.create(
                        room=room,
                        user = myUser,
                        check_in_date=check_in_date,
                        check_out_date=check_out_date
                    )
                    booking.save()
                    return redirect('hms:dashboard')

                else:
                    print('\nNo Rooms Available\n')
    else:
        form = BookingForm()

    data['form'] = form
    data['show_table'] = show_table

    return render(request, 'main/booking.html', data)



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
