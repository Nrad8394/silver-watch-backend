from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Appointment, Reminder, Schedule


class ReminderInline(admin.TabularInline):
    model = Reminder
    extra = 1
    fields = ("type", "scheduled_for", "sent")
    readonly_fields = ("sent",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "provider", "date", "time", "status", "type", "formatted_duration", "location_display")
    list_filter = ("status", "type", "date", "provider")
    search_fields = ("patient__full_name", "provider__full_name", "purpose")
    ordering = ("-date", "time")
    inlines = [ReminderInline]

    fieldsets = (
        (_("Appointment Details"), {
            "fields": ("patient", "provider", "type", "status", "date", "time", "duration", "purpose", "notes")
        }),
        (_("Location & Virtual"), {
            "fields": ("location", "meeting_link"),
        }),
    )

    actions = ["mark_confirmed", "mark_cancelled", "mark_no_show"]

    def formatted_duration(self, obj):
        return f"{obj.duration} min"
    formatted_duration.short_description = "Duration"

    def location_display(self, obj):
        if obj.type == "Virtual":
            return format_html('<a href="{}" target="_blank">Meeting Link</a>', obj.meeting_link) if obj.meeting_link else "N/A"
        return obj.location or "N/A"
    location_display.short_description = "Location"

    @admin.action(description="Mark selected appointments as Confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="Confirmed")

    @admin.action(description="Mark selected appointments as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status="Cancelled")

    @admin.action(description="Mark selected appointments as No-Show")
    def mark_no_show(self, request, queryset):
        queryset.update(status="No-Show")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "availability_summary")
    search_fields = ("user__full_name",)
    ordering = ("user",)

    def availability_summary(self, obj):
        return f"{len(obj.availability)} Days Available"
    availability_summary.short_description = "Availability"



@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("appointment", "type", "scheduled_for", "sent")
    list_filter = ("type", "sent")
    search_fields = ("appointment__patient__full_name",)
    ordering = ("-scheduled_for",)