from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Club, Comment, Event


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css_class} form-control".strip()


class ClubForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Club
        fields = ["club_name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ["event_name", "description", "event_date", "location"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "event_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_event_date(self):
        value = self.cleaned_data["event_date"]
        if value is None:
            return value
        return value


class CommentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add a comment about this event",
                }
            ),
        }


class SignUpForm(StyledFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")
