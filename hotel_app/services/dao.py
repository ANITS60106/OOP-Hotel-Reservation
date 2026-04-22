from django.db.models import Count, Sum
from hotel_app.models import Booking, Category, CheckIn, Room


class CategoryDAO:
    @staticmethod
    def create(**kwargs):
        return Category.objects.create(**kwargs)

    @staticmethod
    def list_all():
        return Category.objects.all()

    @staticmethod
    def update(instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def delete(instance):
        instance.delete()


class RoomDAO:
    @staticmethod
    def create(**kwargs):
        return Room.objects.create(**kwargs)

    @staticmethod
    def list_active():
        return Room.objects.filter(is_active=True).select_related("category").prefetch_related("amenities", "gallery")

    @staticmethod
    def featured():
        return RoomDAO.list_active().filter(featured=True)

    @staticmethod
    def update(instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def delete(instance):
        instance.delete()


class BookingDAO:
    @staticmethod
    def create(**kwargs):
        booking = Booking(**kwargs)
        booking.full_clean()
        booking.save()
        return booking

    @staticmethod
    def list_all():
        return Booking.objects.select_related("room", "customer", "room__category")

    @staticmethod
    def update(instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @staticmethod
    def delete(instance):
        instance.delete()

    @staticmethod
    def reports():
        total_rooms = Room.objects.filter(is_active=True).count()
        available_rooms = sum(1 for room in Room.objects.filter(is_active=True) if not room.is_booked)
        total_bookings = Booking.objects.count()
        revenue = sum(booking.total_price for booking in Booking.objects.exclude(status=Booking.Status.CANCELLED))
        return {
            "summary": {
                "total_rooms": total_rooms,
                "available_rooms": available_rooms,
                "occupied_rooms": total_rooms - available_rooms,
                "total_bookings": total_bookings,
                "active_checkins": CheckIn.objects.filter(checked_out_at__isnull=True).count(),
                "estimated_revenue": revenue,
            },
            "reports": {
                "bookings_by_category": list(Booking.objects.values("room__category__name").annotate(total=Count("id")).order_by("-total")),
                "top_rooms_by_bookings": list(Booking.objects.values("room__title").annotate(total=Count("id")).order_by("-total")[:5]),
                "room_performance": list(Booking.objects.exclude(status=Booking.Status.CANCELLED).values("room__title").annotate(total=Count("id"), gross=Sum("room__price_per_night")).order_by("-total")[:5]),
                "latest_bookings": list(Booking.objects.select_related("room", "customer").values("guest_name", "room__title", "status", "check_in", "check_out")[:5]),
                "status_breakdown": list(Booking.objects.values("status").annotate(total=Count("id")).order_by("-total")),
            },
        }
