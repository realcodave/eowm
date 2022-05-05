from django.urls import path
from django.conf import settings
from .views import Index, About, HallList, Tent, Mission_Hall, Ark, Galleries, RoomList, ProfileView,HallDetailView, HallBookingView, BookingList, HallList, BookingView, CancelBookingView, RoomDetailView
 
urlpatterns = [
    path('', Index, name="index"),
    path('about/', About, name="about"),
    path('halls/', HallList, name="halls"),
    path('tent/', Tent, name="tent"),
    # path('book/mission/', Mission_Hall, name="mission"),
    path('ark/', Ark, name="ark"),
    path('gallery/', Galleries, name="gallery"),
    path("room_list/", RoomList, name='rooms'),
    path('booking_list/', BookingList.as_view(), name="BookingList"),
    path('book/', BookingView.as_view(), name="booking_view"),
    path('hallbook/', HallBookingView.as_view(), name="booking_view"),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name="CancelBookingView"),
    path('room/<str:category>', RoomDetailView.as_view(), name="single_book"),
    path('hall/<str:category>', HallDetailView.as_view(), name="mission"),
    path('profile/', ProfileView, name="profile"),

    ] 
if settings.DEBUG:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
        