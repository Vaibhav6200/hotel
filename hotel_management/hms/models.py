from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



# class CustomUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=100)
#     phone_number = models.CharField(max_length=20)
#     otp_code = models.CharField(max_length=6, unique=True, null=True)
#     email_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.email


class Room(models.Model):
    ROOM_TYPES = [
        ('ac', 'AC'),
        ('nonac', 'NonAC'),
    ]

    ROOM_STATUSES = [
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('dirty', 'Dirty'),
        ('cleaned', 'Cleaned'),
        ('outofservice', 'Out of Service')
    ]
    id = models.AutoField(primary_key=True, editable=False)
    room_no = models.CharField(max_length=5)
    room_status = models.CharField(max_length=20, choices=ROOM_STATUSES)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    beds = models.PositiveIntegerField()
    price = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='room_images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Room {self.room_no} price: {self.price} "


class Booking(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Room {self.room.room_no}"