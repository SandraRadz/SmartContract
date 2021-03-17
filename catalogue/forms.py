from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import SelectMultiple

from accounts.models import User
from catalogue.models import Product


class ProductForm(forms.ModelForm):
    solvers = forms.ModelMultipleChoiceField(queryset=User.objects.filter(status="solver"),
                                             widget=FilteredSelectMultiple("verbose name", is_stacked=False))

    class Meta:
        model = Product
        fields = ["name", "description", "price"]


class SolversForm(forms.Form):
    def __init__(self, product, *args, **kwargs):
        super(SolversForm, self).__init__(*args, **kwargs)
        self.fields['solver'] = forms.ChoiceField(
            choices=[(d.id, d.__str__()) for d in product.solver_list.all()],
            widget=forms.RadioSelect()
        )