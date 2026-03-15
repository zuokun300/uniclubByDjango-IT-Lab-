from django.contrib import admin

from .models import Club, Comment, Event, Membership, Registration


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("club_name", "founded_by", "created_at")
    search_fields = ("club_name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("event_name", "club", "event_date", "created_by")
    list_filter = ("club",)
    search_fields = ("event_name", "location")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("club", "user", "join_date")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "status", "created_at")
    list_filter = ("status",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "created_at")

