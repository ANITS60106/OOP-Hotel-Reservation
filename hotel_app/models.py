from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def room_cover_upload_path(instance, filename):
    return f"rooms/{instance.slug}/cover/{filename}"


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Room(TimeStampedModel):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="rooms")
    summary = models.CharField(max_length=180)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=1)
    room_size = models.PositiveIntegerField()
    beds = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    cover_image = models.ImageField(upload_to=room_cover_upload_path, blank=True, null=True)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["price_per_night", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_booked(self):
        return self.bookings.filter(status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED, Booking.Status.CHECKED_IN]).exists()

    def get_status_label(self):
        return "Booked" if self.is_booked else "Available"

    def __str__(self):
        return self.title


class Booking(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CHECKED_IN = "checked_in", "Checked In"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    guest_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    special_request = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Checkout date must be later than check-in date.")
        if self.guests > self.room.capacity:
            raise ValidationError("Number of guests exceeds room capacity.")
        overlapping = Booking.objects.filter(
            room=self.room,
            status__in=[self.Status.PENDING, self.Status.CONFIRMED, self.Status.CHECKED_IN],
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This room is not available for the selected dates.")

    @property
    def total_nights(self):
        return (self.check_out - self.check_in).days

    @property
    def total_price(self):
        return Decimal(self.total_nights) * self.room.price_per_night

    def mark_checked_in(self):
        self.status = self.Status.CHECKED_IN
        self.save(update_fields=["status", "updated_at"])

    def mark_completed(self):
        self.status = self.Status.COMPLETED
        self.save(update_fields=["status", "updated_at"])

    def __str__(self):
        return f"{self.guest_name} - {self.room.title}"


class Amenity(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    rooms = models.ManyToManyField(Room, related_name="amenities", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


class RoomImage(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="rooms/gallery/")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.room.title} image"


class CheckIn(TimeStampedModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="checkin_record")
    checked_in_at = models.DateTimeField(default=timezone.now)
    checked_out_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-checked_in_at"]

    @property
    def is_active(self):
        return self.checked_out_at is None

    def checkout(self):
        self.checked_out_at = timezone.now()
        self.save(update_fields=["checked_out_at"])
        self.booking.mark_completed()

    def __str__(self):
        return f"{self.booking.guest_name} check-in"
