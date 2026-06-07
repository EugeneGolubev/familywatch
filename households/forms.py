from django import forms

from .models import Household


class HouseholdCreateForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ["name", "default_country"]

    def clean_name(self) -> str:
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Enter a household name.")
        return name

    def clean_default_country(self) -> str:
        return self.cleaned_data["default_country"].upper()
