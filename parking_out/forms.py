from django import forms
from django.db.models.aggregates import Max

from parking_out.models import Parking_expenditure


class Parking_expenditureForm(forms.ModelForm):
    """ models.pyのモデルを追加するためModelFormとする
    https://qiita.com/felyce/items/5042db0792c9f7d01c1e
    """

    max_ki = Parking_expenditure.objects.aggregate(ki=Max('ki'))
    if max_ki["ki"] is None:
        ki = forms.IntegerField(label='期', initial=0)
    else:
        ki = forms.IntegerField(label='期', initial=max_ki["ki"]+1)
    koujimei = forms.CharField(label='支出項目', initial='振替')
    cost = forms.IntegerField(label='支出額')
    comment = forms.CharField(
        label='コメント', widget=forms.Textarea, required=False)

    class Meta:
        model = Parking_expenditure
        fields = ("ki", "account_type", "koujimei", "cost", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input is-size-6"
        self.fields['account_type'].widget.attrs["class"] = "select-css is-size-6"
        self.fields['koujimei'].widget.attrs["class"] = "input is-size-6"
        self.fields['cost'].widget.attrs["class"] = "input is-size-6"
        self.fields['comment'].widget.attrs["class"] = "text is-size-6"
