from django import forms
from django.db.models.aggregates import Max

from parking_in.models import Parking_income


class Parking_incomeForm(forms.ModelForm):
    """ models.pyのモデルを追加するためModelFormとする
    https://qiita.com/felyce/items/5042db0792c9f7d01c1e
    """
    max_ki = Parking_income.objects.aggregate(ki=Max('ki'))
    if max_ki["ki"] is None:
        ki = forms.IntegerField(label='期', initial=0)
    else:
        ki = forms.IntegerField(label='期', initial=max_ki["ki"]+1)

    parking_lot_income = forms.IntegerField(label='収入額')

    class Meta:
        model = Parking_income
        fields = ("ki", "parking_lot_income")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input is-size-6"
        self.fields['parking_lot_income'].widget.attrs["class"] = "input is-size-6"
