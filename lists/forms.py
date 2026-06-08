from django import forms

from catalog.models import Title
from lists.models import HouseholdList, UserTitleState
from lists.services import HouseholdListService


class PersonalTitleStateForm(forms.ModelForm):
    class Meta:
        model = UserTitleState
        fields = ["status", "rating", "notes", "watched_at"]
        widgets = {
            "status": forms.Select(attrs={"class": "w-full rounded bg-slate-900 border border-slate-700 p-2"}),
            "rating": forms.NumberInput(
                attrs={"class": "w-full rounded bg-slate-900 border border-slate-700 p-2", "min": 1, "max": 10}
            ),
            "notes": forms.Textarea(attrs={"class": "w-full rounded bg-slate-900 border border-slate-700 p-2", "rows": 3}),
            "watched_at": forms.DateTimeInput(
                attrs={"class": "w-full rounded bg-slate-900 border border-slate-700 p-2", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].required = False
        self.fields["watched_at"].required = False

    def clean_rating(self) -> int | None:
        rating = self.cleaned_data.get("rating")
        if rating is not None and not 1 <= rating <= 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return rating

    def clean_watched_at(self):
        watched_at = self.cleaned_data.get("watched_at")
        status = self.cleaned_data.get("status")
        if status != UserTitleState.Status.WATCHED:
            return None
        return watched_at


class HouseholdListCreateForm(forms.ModelForm):
    class Meta:
        model = HouseholdList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded bg-slate-900 border border-slate-700 p-2"}),
        }

    def clean_name(self) -> str:
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Enter a list name.")
        return name


class HouseholdCategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: HouseholdList) -> str:
        return f"{obj.household.name} - {obj.name}"


class HouseholdCategoryChoiceForm(forms.Form):
    household_list = HouseholdCategoryChoiceField(
        label="Household category",
        queryset=HouseholdList.objects.none(),
        widget=forms.Select(attrs={"class": "w-full rounded bg-slate-900 border border-slate-700 p-2"}),
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["household_list"].queryset = HouseholdListService.categories_for_user(user=user)


class TMDbTitleAddForm(forms.Form):
    media_type = forms.ChoiceField(choices=Title.Type.choices, widget=forms.HiddenInput)
    tmdb_id = forms.IntegerField(widget=forms.HiddenInput)
