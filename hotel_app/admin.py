from django.contrib import admin
from .models import Amenity, Booking, Category, CheckIn, Room, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price_per_night", "capacity", "featured", "is_active")
    list_filter = ("category", "featured", "is_active")
    search_fields = ("title", "summary", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [RoomImageInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("guest_name", "room", "check_in", "check_out", "guests", "status")
    list_filter = ("status", "room__category")
    search_fields = ("guest_name", "email", "phone_number", "room__title")


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ("booking", "checked_in_at", "checked_out_at")
    list_filter = ("checked_out_at",)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
