from datetime import date, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Booking, Category, Room


class BookingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="secret123")
        self.category = Category.objects.create(name="Deluxe")
        self.room = Room.objects.create(title="Ocean Deluxe", category=self.category, summary="Great room", description="Large modern room", price_per_night=120, capacity=2, room_size=32, beds=1, bathrooms=1)

    def test_total_nights_and_total_price(self):
        booking = Booking.objects.create(customer=self.user, room=self.room, guest_name="Ray", phone_number="123", email="ray@example.com", check_in=date.today() + timedelta(days=1), check_out=date.today() + timedelta(days=4), guests=2, status=Booking.Status.CONFIRMED)
        self.assertEqual(booking.total_nights, 3)
        self.assertEqual(float(booking.total_price), 360.0)

    def test_invalid_date_range_raises_error(self):
        booking = Booking(customer=self.user, room=self.room, guest_name="Ray", phone_number="123", email="ray@example.com", check_in=date.today() + timedelta(days=3), check_out=date.today() + timedelta(days=1), guests=1, status=Booking.Status.CONFIRMED)
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_capacity_validation_raises_error(self):
        booking = Booking(customer=self.user, room=self.room, guest_name="Ray", phone_number="123", email="ray@example.com", check_in=date.today() + timedelta(days=1), check_out=date.today() + timedelta(days=2), guests=5, status=Booking.Status.CONFIRMED)
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_room_booking_status_updates(self):
        self.assertFalse(self.room.is_booked)
        Booking.objects.create(customer=self.user, room=self.room, guest_name="Ray", phone_number="123", email="ray@example.com", check_in=date.today() + timedelta(days=1), check_out=date.today() + timedelta(days=2), guests=2, status=Booking.Status.CONFIRMED)
        self.assertTrue(Room.objects.get(pk=self.room.pk).is_booked)
