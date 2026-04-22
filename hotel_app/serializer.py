from rest_framework import serializers
from .models import Amenity, Booking, Category, CheckIn, Room, RoomImage


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name"]


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ["id", "image"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class RoomSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    gallery = RoomImageSerializer(many=True, read_only=True)
    is_booked = serializers.BooleanField(read_only=True)
    status_label = serializers.CharField(source="get_status_label", read_only=True)

    class Meta:
        model = Room
        fields = ["id", "title", "slug", "category", "summary", "description", "price_per_night", "capacity", "room_size", "beds", "bathrooms", "cover_image", "featured", "is_active", "is_booked", "status_label", "amenities", "gallery"]


class BookingSerializer(serializers.ModelSerializer):
    total_nights = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    room_detail = RoomSerializer(source="room", read_only=True)
    customer_name = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "customer", "customer_name", "room", "room_detail", "guest_name", "phone_number", "email", "check_in", "check_out", "guests", "special_request", "status", "total_nights", "total_price", "created_at"]
        read_only_fields = ["customer", "status", "created_at"]

    def validate(self, attrs):
        room = attrs.get("room")
        guests = attrs.get("guests", 1)
        if room and guests > room.capacity:
            raise serializers.ValidationError({"guests": "Too many guests for this room."})
        return attrs


class CheckInSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    room_title = serializers.CharField(source="booking.room.title", read_only=True)
    guest_name = serializers.CharField(source="booking.guest_name", read_only=True)

    class Meta:
        model = CheckIn
        fields = ["id", "booking", "room_title", "guest_name", "checked_in_at", "checked_out_at", "is_active"]
