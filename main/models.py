from django.db.models.base import Model
from django.urls import reverse
from django.db import models
from django.conf import settings
import secrets
# Create your models here.
class Rooms(models.Model):
    ROOM_CATEGORIES = (
        ('SC', 'SELF CONTAINED'),
        ('SR', 'SINGLE ROOM'),
        ('DA', 'DORMITORY BUNKS (80)'),
        ('DB', 'DORMITORY BUNKS (40)'),
        ('DC', 'DORMITORY BUNKS (40)'),
        
        
    )
    rooms = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=2, choices=ROOM_CATEGORIES)
    beds = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return f'room {self.rooms} {self.category} with {self.beds} bed and capacity {self.capacity}'

class Halls(models.Model):
    HALL_CATEGORIES = (
        ('KH', 'KINGDOM HALL'),
        ('MH', 'MISSION HALL'),
    )
    halls = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=2, choices=HALL_CATEGORIES)
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.category} can contain {self.capacity} people '


class Booking(models.Model):
    HALL_CATEGORIES = (
        ('KH', 'KINGDOM HALL'),
        ('MH', 'MISSION HALL'),
    )
    ROOM_CATEGORIES = (
        ('SC', 'SELF CONTAINED'),
        ('SR', 'SINGLE ROOM'),
        ('DA', 'DORMITORY BUNKS (80)'),
        ('DB', 'DORMITORY BUNKS (40)'),
        ('DC', 'DORMITORY BUNKS (40)'),
        
        
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, blank=True, null = True, on_delete=models.CASCADE)
    hall = models.ForeignKey(Halls, blank=True, null = True, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.user} has booked {(self.room ) or (self.hall)} from {self.check_in} to {self.check_out}' 
    
    def get_room_category(self):
        room_categories = dict(self.ROOM_CATEGORIES).get(self.room.category)
        return room_categories

    def get_hall_category(self):
        hall_categories = dict(self.HALL_CATEGORIES).get(self.hall.category)
        return hall_categories

    def get_cancel_booking_url(self):
        return reverse('CancelBookingView', args=[self.pk])

class Gallery(models.Model):
    
    image = models.ImageField(upload_to='images')


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=15)
    surName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    telephone1 = models.CharField(max_length=250)
    telephone2 = models.CharField(max_length=250, blank=True, null=True)
    contact_name = models.CharField(max_length=30)
    contact_address = models.CharField(max_length=250)
    contact_phone = models.CharField(max_length=250)
    relationship = models.CharField(max_length=250)
    idCard = models.ImageField(upload_to='images/id')

    def __str__(self):
        return f'{self.title} {self.surName} {self.firstName} '

class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref = models.CharField()
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)
    
    def __str__(self):
        return f"Payment: {self.amount}"
    
    def save(save, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref 
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount
            