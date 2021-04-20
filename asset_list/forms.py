from django import forms
from django.db.models.aggregates import Max
from asset_list.models import AssetList, Master_assetlist


class AssetListForm(forms.ModelForm):
    """ 資産データ用のForm """
    # 本来はview関数で初期値を設定すべきか?
    max_ki = AssetList.objects.aggregate(ki=Max('ki'))
    if max_ki["ki"] is None:
        ki = forms.IntegerField(label='期', initial=0)
    else:
        ki = forms.IntegerField(label='期', initial=max_ki["ki"]+1)

    class Meta:
        model = AssetList
        fields = ('ki', 'account_type', 'master', 'asset', 'comment',)
        labels = {
            'account_type': '会計区分',
            'master': '資産種別',
            'asset': '資産額',
            'comment': '説明',
        }

    # fieldにbootstrap用のclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input"
        self.fields['account_type'].widget.attrs["class"] = "select-css"
        self.fields['master'].widget.attrs["class"] = "select-css"
        self.fields['asset'].widget.attrs["class"] = "input"
        self.fields['comment'].widget.attrs["class"] = "textarea"
        self.fields['comment'].widget.attrs["rows"] = "4"


class Master_assetForm(forms.ModelForm):
    """ 資産マスターの登録用フォーム """
    name = forms.CharField(label='口座名', max_length=64)
    account_number = forms.CharField(label='口座番号', max_length=24, initial='-')
    sequense = forms.IntegerField(label='表示順序')
    isAsset = forms.IntegerField(label='資産(1)/負債(0)', initial=1)
    alive = forms.NullBooleanField(label='有効', initial=True)

    class Meta:
        model = Master_assetlist
        fields = ("sequense", "name", "account_number", "isAsset", "alive", "comment")
        labels = {
            'comment': '備考',
        }
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': '3',
            })
        }

    # fieldにclassを一括設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs["class"] = "input"
        self.fields['account_number'].widget.attrs["class"] = "input"
        self.fields['sequense'].widget.attrs["class"] = "input"
        self.fields['isAsset'].widget.attrs["class"] = "input"
        self.fields['alive'].widget.attrs["class"] = "select"
        self.fields['comment'].widget.attrs["class"] = "textarea"


class BalanceSheetForm(forms.Form):
    """ 貸借対照表の期 """
    ki = forms.IntegerField(
        label='期',
        widget=forms.NumberInput(attrs={'style': 'width: 12ch'}),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input is-small"
