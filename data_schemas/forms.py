from django import forms
from .models import DataSchema, DataColumn
from django.forms.models import inlineformset_factory


class DataColumnForm(forms.ModelForm):
    """A form class for DataColumn"""

    class Meta:
        model = DataColumn
        exclude = ('user',)


DataColumnFormSet = inlineformset_factory(DataSchema, DataColumn, fields=(
    'name', 'data_type', 'sentences_num', 'start_num', 'end_num', 'order'
), extra=1, can_delete=True)


class DataSchemaForm(forms.ModelForm):
    """A form class for DataSchema"""

    class Meta:
        model = DataSchema
        fields = ('name',)
