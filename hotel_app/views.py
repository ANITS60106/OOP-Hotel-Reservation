from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking, CheckIn
from .serializer import BookingSerializer, CheckInSerializer, RoomSerializer
from .services.dao import BookingDAO, RoomDAO


class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = RoomDAO.list_active()
        category = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")
        capacity = self.request.query_params.get("capacity")
        max_price = self.request.query_params.get("max_price")
        if category:
            queryset = queryset.filter(category__slug=category)
        if featured == "true":
            queryset = queryset.filter(featured=True)
        if capacity:
            queryset = queryset.filter(capacity__gte=capacity)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        return queryset


class RoomDetailView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return RoomDAO.list_active()


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save(customer=self.request.user, status=Booking.Status.CONFIRMED)
        booking.full_clean()
        booking.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Booking created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookingDAO.list_all().filter(customer=self.request.user)


class DashboardCheckInView(generics.ListAPIView):
    serializer_class = CheckInSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return CheckIn.objects.select_related("booking", "booking__room", "booking__customer")


class CheckInView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.mark_checked_in()
        checkin, created = CheckIn.objects.get_or_create(booking=booking)
        if not created and checkin.checked_out_at is not None:
            checkin.checked_out_at = None
            checkin.save(update_fields=["checked_out_at"])
        return Response({"message": "Guest checked in successfully."})


class CheckoutView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)
        record = get_object_or_404(CheckIn, booking=booking)
        record.checkout()
        return Response({"message": "Checkout completed successfully."})


class ReportsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response(BookingDAO.reports())
