from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Session


class SessionForm(forms.ModelForm):
    """An input form built automatically from the Session model's fields."""

    class Meta:
        model = Session  # Build the form from this model.
        # Which fields the user may fill, in this order. "user" is NOT here on purpose:
        # the owner is set in the view from request.user, so nobody can fake it.
        fields = ["course", "minutes", "note", "day"]
        widgets = {
            # Show a real date picker in the browser instead of a plain text box.
            "day": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
        # The labels shown above each field. Display only: the database doesn't change.
        labels = {
            "course": "الدورة",
            "minutes": "الدقائق",
            "note": "ملاحظة",
            "day": "التاريخ",
        }

    def __init__(self, *args, **kwargs):
        # First, let Django build the form normally (inheritance, like Python 103).
        super().__init__(*args, **kwargs)
        # Then loop over every field and give it a Bootstrap style class.
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"  # Dropdown lists.
            else:
                field.widget.attrs["class"] = "form-control"  # Normal input boxes.
        # The first, empty choice in the course dropdown.
        self.fields["course"].empty_label = "اختر الدورة"


class SignupForm(UserCreationForm):
    """Django's ready-made signup form, with Bootstrap styling added."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Same trick as SessionForm: give every input Bootstrap's look.
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"