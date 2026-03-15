from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ClubForm, CommentForm, EventForm, SignUpForm
from .models import Club, Comment, Event, Membership, Registration


class HomeView(ListView):
    model = Club
    template_name = "core/home.html"
    context_object_name = "clubs"

    def get_queryset(self):
        return (
            Club.objects.select_related("founded_by")
            .prefetch_related("events", "memberships")
            .order_by("club_name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.select_related("club").order_by("event_date")[:6]
        context["club_count"] = Club.objects.count()
        context["event_count"] = Event.objects.count()
        context["registration_count"] = Registration.objects.count()
        user = self.request.user
        context["member_club_ids"] = set()
        if user.is_authenticated:
            context["member_club_ids"] = set(
                Membership.objects.filter(user=user).values_list("club_id", flat=True)
            )
        return context


class ClubListView(ListView):
    model = Club
    template_name = "core/club_list.html"
    context_object_name = "clubs"

    def get_queryset(self):
        queryset = Club.objects.select_related("founded_by").prefetch_related("events", "memberships")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(club_name__icontains=query)
        return queryset.order_by("club_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["member_club_ids"] = set()
        if user.is_authenticated:
            context["member_club_ids"] = set(
                Membership.objects.filter(user=user).values_list("club_id", flat=True)
            )
        return context


class ClubDetailView(DetailView):
    model = Club
    template_name = "core/club_detail.html"
    context_object_name = "club"

    def get_queryset(self):
        return Club.objects.select_related("founded_by").prefetch_related(
            "memberships__user",
            "events__registrations",
            "events__comments__user",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        user = self.request.user
        events = list(self.object.events.all())
        user_id = user.id if user.is_authenticated else None
        for event in events:
            registrations = list(event.registrations.all())
            event.confirmed_count = sum(
                registration.status == Registration.STATUS_CONFIRMED
                for registration in registrations
            )
            event.user_registration = next(
                (registration for registration in registrations if registration.user_id == user_id),
                None,
            )
            event.user_registration_status = (
                event.user_registration.status if event.user_registration else None
            )

        context["events"] = events
        context["is_member"] = (
            user.is_authenticated
            and Membership.objects.filter(club=self.object, user=user).exists()
        )
        context["can_create_event"] = user.is_authenticated and self.object.founded_by_id == user.id
        return context


class ClubCreateView(LoginRequiredMixin, CreateView):
    model = Club
    form_class = ClubForm
    template_name = "core/form.html"

    def form_valid(self, form):
        form.instance.founded_by = self.request.user
        response = super().form_valid(form)
        Membership.objects.get_or_create(club=self.object, user=self.request.user)
        messages.success(self.request, "Club created successfully.")
        return response


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "core/form.html"

    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(Club, pk=kwargs["club_pk"])
        if self.club.founded_by_id != request.user.id:
            raise PermissionDenied("Only the club founder can create events.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.club = self.club
        form.instance.created_by = self.request.user
        messages.success(self.request, "Event created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.club.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = f"Add event for {self.club.club_name}"
        return context


class EventFounderRequiredMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Event.objects.select_related("club__founded_by")

    def dispatch(self, request, *args, **kwargs):
        self.event = self.get_object()
        if self.event.club.founded_by_id != request.user.id:
            raise PermissionDenied("Only the club founder can manage this event.")
        return super().dispatch(request, *args, **kwargs)


class EventUpdateView(EventFounderRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "core/form.html"

    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.event.club.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = f"Edit event: {self.event.event_name}"
        return context


class EventDeleteView(EventFounderRequiredMixin, DeleteView):
    model = Event
    template_name = "core/event_confirm_delete.html"

    def get_success_url(self):
        return self.event.club.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Event deleted successfully.")
        return super().delete(request, *args, **kwargs)


class MyRegistrationsView(LoginRequiredMixin, ListView):
    model = Registration
    template_name = "core/my_registrations.html"
    context_object_name = "registrations"

    def get_queryset(self):
        return (
            Registration.objects.select_related("event__club")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created successfully.")
        return response


@login_required
@require_POST
def join_club(request, pk):
    club = get_object_or_404(Club, pk=pk)
    Membership.objects.get_or_create(club=club, user=request.user)
    messages.success(request, f"You joined {club.club_name}.")
    return redirect("club_detail", pk=pk)


@login_required
@require_POST
def register_event(request, pk):
    event = get_object_or_404(Event.objects.select_related("club"), pk=pk)
    registration, created = Registration.objects.get_or_create(
        event=event,
        user=request.user,
        defaults={"status": Registration.STATUS_CONFIRMED},
    )
    if not created and registration.status != Registration.STATUS_CONFIRMED:
        registration.status = Registration.STATUS_CONFIRMED
        registration.save(update_fields=["status"])

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "ok": True,
                "registered": True,
                "event": event.event_name,
                "count": event.registrations.filter(status=Registration.STATUS_CONFIRMED).count(),
            }
        )

    messages.success(request, f"Registration confirmed for {event.event_name}.")
    return redirect("club_detail", pk=event.club_id)


@login_required
@require_POST
def add_comment(request, pk):
    event = get_object_or_404(Event.objects.select_related("club"), pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.event = event
        comment.user = request.user
        comment.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "ok": True,
                    "author": request.user.username,
                    "content": comment.content,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                }
            )
        messages.success(request, "Comment posted.")
    else:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        messages.error(request, "Please enter a comment before submitting.")
    return redirect("club_detail", pk=event.club_id)


@login_required
@require_POST
def cancel_registration(request, pk):
    registration = get_object_or_404(
        Registration.objects.select_related("event__club"), pk=pk, user=request.user
    )
    if registration.status != Registration.STATUS_CANCELLED:
        registration.status = Registration.STATUS_CANCELLED
        registration.save(update_fields=["status"])
        messages.success(request, f"Registration cancelled for {registration.event.event_name}.")
    return redirect("my_registrations")
