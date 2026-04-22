from django.urls import path
from .views import BookingCreateView, CheckInView, CheckoutView, DashboardCheckInView, MyBookingsView, ReportsView, RoomDetailView, RoomListView

app_name = "hotel_app"

urlpatterns = [
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("rooms/<slug:slug>/", RoomDetailView.as_view(), name="room-detail"),
    path("bookings/", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/me/", MyBookingsView.as_view(), name="my-bookings"),
    path("dashboard/checkins/", DashboardCheckInView.as_view(), name="dashboard-checkins"),
    path("dashboard/checkin/<int:booking_id>/", CheckInView.as_view(), name="checkin"),
    path("dashboard/checkout/<int:booking_id>/", CheckoutView.as_view(), name="checkout"),
    path("dashboard/reports/", ReportsView.as_view(), name="reports"),
]
