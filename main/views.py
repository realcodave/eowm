from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from operator import attrgetter
from django.views.generic import TemplateView, ListView, FormView, View, DeleteView
from .models import Gallery, Profile, Rooms, Booking, Halls, Payment
from .forms import AvailabilityForm, ProfileForm, HallAvailabilityForm, PaymentForm
from main.booking_functions.availability import check_availability, hall_availability
from django.urls import reverse, reverse_lazy

# Create your views here.

def Index(request):
    return render(request, 'index.html')

def About(request):
    return render(request, 'about.html')


# def MissionHall(request):
#     return render

# def KingdomHall(request):
#     return render

# def SingleRooms(request):
#     return render(request, '')

# def SelfContained(request):
#     return render

# def Dormitory(request):
#     return render

class BookingList(ListView):
    model = Booking
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            
            return booking_list
        else:
            booking_list = Booking.objects.filter(user = self.request.user)
            return booking_list

class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = "availability_form.html"

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Rooms.objects.filter(category=data['room_category'])
        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
        if len(available_rooms) > 0:
            room  = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('This Categories of rooms are booked try another one')

class HallBookingView(FormView):
    form_class = HallAvailabilityForm
    template_name = "hall_availability_form.html"

    def form_valid(self, form):
        data = form.cleaned_data
        hall_list = Halls.objects.filter(category=data['hall_category'])
        available_halls = []
        for hall in hall_list:
            if hall_availability(hall, data['check_in'], data['check_out']):
                available_halls.append(hall)
        if len(available_halls) > 0:
            room  = available_halls[0]
            booking = Booking.objects.create(
                user = self.request.user,
                hall = hall,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('This Categories of rooms are booked try another one')

class SingleBookingViewRoom(FormView):
    form_class = AvailabilityForm
    template_name = "room_availability_form.html"

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Rooms.objects.filter(category=data['room_category'])
        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
        if len(available_rooms) > 0:
            room  = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('This Categories of rooms are booked try another one')



def HallList(request):
    context = {}
    hall_list = Halls.objects.all()
    context['hall_list'] = hall_list
    return render(request, 'halls.html', context)

class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        profile = Profile.objects.filter(user = request.user)
        if profile:
            form = AvailabilityForm()
            room_list = Rooms.objects.filter(category=category)
            if len(room_list) > 0:
                room = room_list[0]
                room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
                context = {
                    'room_category' : room_category,
                    'form' : form
                }
                return render(request, 'room_detail_view.html', context)
            return HttpResponse('Category Does Not Exist')
        else:
            return HttpResponseRedirect(reverse("profile"))

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        rooms_list = Rooms.objects.filter(category=category)
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        available_rooms = []
        for room in rooms_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
        if len(available_rooms) > 0:
            room  = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponseRedirect(reverse("BookingList"))
        else:
            return HttpResponse('This Categories of roomss are booked try another one')

class HallDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        profile = Profile.objects.filter(user = request.user)
        if profile:
            form = HallAvailabilityForm()
            hall_list = Halls.objects.filter(category=category)
            if len(hall_list) > 0:
                hall = hall_list[0]
                hall_category = dict(hall.HALL_CATEGORIES).get(hall.category, None)
                context = {
                    'hall_category' : hall_category,
                    'form' : form
                }
                return render(request, 'hall_detail_view.html', context)
            return HttpResponse('Category Does Not Exist')
        else:
            return HttpResponseRedirect(reverse("profile"))



    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        hall_list = Halls.objects.filter(category=category)
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        available_halls = []
        for hall in hall_list:
            if hall_availability(hall, data['check_in'], data['check_out']):
                available_halls.append(hall)
        if len(available_halls) > 0:
            hall  = available_halls[0]
            booking = Booking.objects.create(
                user = self.request.user,
                hall = hall,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponseRedirect(reverse("BookingList"))
        else:
            return HttpResponse('This Categories of halls are booked try another one')
        
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_confirm_delete.html'
    success_url = reverse_lazy('BookingList')

def RoomList(request):
    context = {}
    room_list = Rooms.objects.all()
    context['room_list'] = room_list
    return render(request, 'rooms.html', context)

def Tent(request):
    return render(request, 'tents.html')

def Mission_Hall(request):
    return render(request, 'mission_booking.html')

def Ark(request):
    return render(request, 'feature.html')

def Galleries(request):
    context = {}
    gallery = Gallery.objects.all().order_by('-id')
    context['gallery'] = gallery
    return render(request, 'class.html', context)


def ProfileView(request):
    context = {}
    form = ProfileForm()
    if request.method == "POST":
        
        form = ProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            title = form.cleaned_data.get('title')
            surName = form.cleaned_data.get('surName')
            firstName = form.cleaned_data.get('firstName')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            telephone1 = form.cleaned_data.get('telephone1')
            telephone2 = form.cleaned_data.get('telephone2')
            contact_name = form.cleaned_data.get('contact_name')
            contact_address = form.cleaned_data.get('contact_address')
            contact_phone = form.cleaned_data.get('contact_phone')
            relationship = form.cleaned_data.get('relationship')
            idCard = form.cleaned_data.get("idCard")
            obj = Profile.objects.create(
                user = request.user,
                title = title,
                surName = surName, 
                firstName = firstName,
                address = address,
                city = city,
                country = country,
                telephone1 = telephone1, 
                telephone2 = telephone2,
                contact_name = contact_name,
                contact_address = contact_address, 
                contact_phone = contact_phone,
                relationship = relationship,
                idCard = idCard,
            )
            
            obj.save()
            
            
    profile = Profile.objects.filter(user=request.user)
    context['form'] = form
    context['profile'] = profile
    return render(request, 'profile.html', context)


# class ProfileView(View):
#     def get(self, request, *args, **kwargs):
#         form = ProfileForm()
#         profile = Profile.objects.filter(user=request.user)
        
#         context = {
#                 'form' : form
#             }
#         return render(request, 'profile.html', context)
        


#     def post(self, request, *args, **kwargs):
#         profile = Profile.objects.filter(user=request.user)
#         form = ProfileForm(request.POST)
#         print(form)
#         if form.is_valid():
#             data = form.cleaned_data
        
#             save_profile = Profile.objects.create(
#                 user = self.request.user,
#                 title = data['title']
#             )
#             save_profile.save()
        
#         return HttpResponse('<h1 style="color: green">Profile Updated </h1>')

def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request == "POST":
        # payment = forms.
        pass
