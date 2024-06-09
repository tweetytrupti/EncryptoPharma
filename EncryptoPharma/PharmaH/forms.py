from django import forms
from .models import Component,Details

# class ComponentForm(forms.ModelForm):
#     class Meta:
#         model = Component
#         fields = ['name', 'quantity', 'cost']

class ComponentForm(forms.ModelForm):
    # name = forms.ModelChoiceField(queryset=Details.objects.none())

    class Meta:
        model = Component
        fields = ['name', 'quantity', 'cost']

    # def __init__(self, *args, **kwargs):
    #     manager = kwargs.pop('manager', None)
    #     super(ComponentForm, self).__init__(*args, **kwargs)
    #     if manager:
    #         self.fields['name'].queryset = Details.objects.filter(manager=manager)
