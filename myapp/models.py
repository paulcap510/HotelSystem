from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    reservations = models.ManyToManyField('Reservation', through='RoomReservation', related_name='room_set')

    def __str__(self):
        return self.room_number

class Reservation(models.Model):
    guest_name = models.CharField(max_length=100)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservation_set')
    credit_card_number = models.CharField(max_length=16)
    security_code = models.CharField(max_length=3)
    name_on_card = models.CharField(max_length=100)
    expiration_date = models.CharField(max_length=100)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Add this field

    def __str__(self):
        return self.guest_name
    
class RoomReservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    date = models.DateField()