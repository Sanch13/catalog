from django import forms

from catalog.models.cap import Cap


class CapFilterForm(forms.Form):
    type_of_closure = forms.MultipleChoiceField(
        choices=Cap.TypeOfClosure.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    throat_standard = forms.MultipleChoiceField(
        choices=Cap.ThroatStandard.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    surface = forms.MultipleChoiceField(
        choices=Cap.SurfaceCap.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
