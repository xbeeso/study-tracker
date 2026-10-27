from django import forms

from .models import Session


class SessionForm(forms.ModelForm):
    """An input form built automatically from the Session model's fields."""

    class Meta:
        model = Session  # Build the form from this model.
        fields = ["course", "minutes", "note", "day"]  # Which fields to show, in this order.
        widgets = {
            # Show a real date picker in the browser instead of a plain text box.
            "day": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
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


    class Meta:
        model = Session  # Build the form from this model.
        fields = ["course", "minutes", "note", "day"]  # Which fields to show, in this order.
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