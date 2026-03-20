from django import forms
from .models import WasteItem, WasteCategory


class WasteItemForm(forms.ModelForm):
    class Meta:
        model = WasteItem
        fields = ['title', 'category', 'description', 'quantity', 'unit',
                  'price_per_unit', 'location', 'possible_products', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'possible_products': forms.Textarea(attrs={'rows': 3,
                'placeholder': 'e.g. Compost, Biofertilizer, Biogas, Animal Feed'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                continue
            field.widget.attrs['class'] = 'form-control'


class SearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search waste products...'
    }))
    category = forms.ModelChoiceField(
        queryset=WasteCategory.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status'), ('available', 'Available'), ('sold', 'Sold'), ('pending', 'Pending')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
