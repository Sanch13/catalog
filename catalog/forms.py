from django import forms

from catalog.models import Bottle
from catalog.models.cap import Cap
from catalog.models.jar import Jar

from catalog.utils import get_validate_list_values


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


class JarFilterForm(forms.Form):
    volume = forms.MultipleChoiceField(
        choices=Jar.VolumeFilterJar.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    surface = forms.MultipleChoiceField(
        choices=Jar.SurfaceJar.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    status_decoration = forms.MultipleChoiceField(
        choices=Jar.DecorationFilterJar.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def clean_volume(self):
        data = self.cleaned_data['volume']
        return get_validate_list_values(data=data)

    def clean_status_decoration(self):
        data = self.cleaned_data['status_decoration']
        return Jar.YesNoStatusJar.YES if 'декорирование' in data else None


filtered_choices = [
    (Bottle.ShapeBottle.CYLINDER, Bottle.ShapeBottle.CYLINDER.label),
    (Bottle.ShapeBottle.RECTANGULAR, Bottle.ShapeBottle.RECTANGULAR.label),
]


class BottlesFilterForm(forms.Form):
    volume = forms.MultipleChoiceField(
        choices=Bottle.VolumeFilterBottle.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    throat_standard = forms.MultipleChoiceField(
        choices=Bottle.ThroatStandard.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    status_decoration = forms.MultipleChoiceField(
        choices=Bottle.DecorationFilterBottle.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    surface = forms.MultipleChoiceField(
        choices=Bottle.SurfaceBottle.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    shape = forms.MultipleChoiceField(
        choices=filtered_choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def clean_volume(self):
        data = self.cleaned_data['volume']
        return get_validate_list_values(data=data)

    def clean_status_decoration(self):
        data = self.cleaned_data['status_decoration']
        return Bottle.YesNoStatusBottle.YES if 'декорирование' in data else None


class ContactLidForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше ФИО', required=True)
    company = forms.CharField(max_length=100, label='Компания', required=True)
    phone_number = forms.CharField(max_length=20,
                                   label='Номер телефона',
                                   required=True)
    email = forms.CharField(max_length=100, label='Ваш e-mail', required=True)

    comment = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 5,  # Указываем количество строк
            'cols': 40  # Указываем количество столбцов (если это нужно)
        })
    )

    def __init__(self, *args, **kwargs):
        super(ContactLidForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'my-form-control'


department_choices = [
    ('', ''),
    ('production_email', 'Продажа оборудования'),
    ('buying_email', 'Сообщение для закупок'),
    ('marketing_email', 'Сообщение для маркетинга'),
    ('miran_email', 'Общие вопросы'),
]


class SupplierForm(forms.Form):
    name_sup = forms.CharField(max_length=100, label='Ваше ФИО', required=True)
    company_sup = forms.CharField(max_length=100, label='Компания', required=True)
    email_sup = forms.CharField(max_length=100, label='Ваш e-mail', required=True)
    department_sup = forms.ChoiceField(choices=department_choices,
                                       label='Отдел',
                                       required=True,
                                       initial=department_choices[0][0])

    comment_sup = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 5,  # Указываем количество строк
            'cols': 40  # Указываем количество столбцов (если это нужно)
        })
    )

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'my-form-control'
            if field_name == "department_sup":
                filed.widget.attrs['class'] += ' my-form-select'


class ContactPriceForm(ContactLidForm):
    def __init__(self, *args, **kwargs):
        super(ContactPriceForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'my-form-control'
            filed.widget.attrs['id'] = f'id_{field_name}_price'
