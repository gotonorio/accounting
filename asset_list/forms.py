from django import forms
from django.db.models.aggregates import Max
from asset_list.models import AssetList, Master_assetlist


class AssetListForm(forms.ModelForm):
    """ 資産データ追加用のFormを宣言
        https://qiita.com/felyce/items/5042db0792c9f7d01c1e
    """
    max_ki = AssetList.objects.aggregate(ki=Max('ki'))
    if max_ki["ki"] is None:
        ki = forms.IntegerField(label='期', initial=0)
    else:
        ki = forms.IntegerField(label='期', initial=max_ki["ki"]+1)
    # 以下はtemplatesでformフィールド名を表示させるため。無くても表示がmodelsの要素名になるだけ。
    master = forms.ModelChoiceField(
        queryset=Master_assetlist.objects.filter(alive=True).order_by('sequense'),
        label='資産種別'
    )
    asset = forms.IntegerField(label='資産額')

    # インナークラスでmodel、fieldを指定する。（これでモデルに紐づける）
    # （https://djangogirlsjapan.gitbooks.io/workshop_tutorialjp/content/django_forms/）
    class Meta:
        model = AssetList
        fields = ('ki', 'account_type', 'master', 'asset', 'comment',)

    # fieldにbootstrap用のclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input"
        self.fields['account_type'].widget.attrs["class"] = "select-css"
        self.fields['master'].widget.attrs["class"] = "select-css"
        self.fields['asset'].widget.attrs["class"] = "input"
        self.fields['comment'].widget.attrs["class"] = "textarea"
        self.fields['comment'].widget.attrs["rows"] = "4"

    # 重複登録をチェックする。
    def clean(self):
        cleaned_data = super().clean()
        ki = cleaned_data['ki']
        master = cleaned_data['master']
        ac_type = cleaned_data['account_type']
        data = AssetList.objects.filter(ki=ki, master=master, account_type=ac_type)
        if data:
            raise forms.ValidationError("既に登録済みです。")
        return cleaned_data


class Master_assetForm(forms.ModelForm):
    """ 資産マスターの登録用フォーム """
    # フィールド名を設定するためにlabelを追加。
    name = forms.CharField(label='口座名', max_length=128)
    account_number = forms.CharField(label='口座番号', max_length=24, initial='-')
    sequense = forms.IntegerField(label='表示順序')
    isAsset = forms.IntegerField(label='資産/負債', initial=1)
    alive = forms.BooleanField(label='有効', required=False)

    class Meta:
        model = Master_assetlist
        fields = ("sequense", "name", "account_number", "isAsset", "alive", "comment")

    # fieldにclassを一括設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs["class"] = "input is-size-6"
        self.fields['account_number'].widget.attrs["class"] = "input is-size-6"
        self.fields['sequense'].widget.attrs["class"] = "input is-size-6"
        self.fields['isAsset'].widget.attrs["class"] = "input is-size-6"
        self.fields['alive'].widget.attrs["class"] = "is-size-6"
        self.fields['comment'].widget.attrs["class"] = "text is-size-6"
        # for field in self.fields.values():
        #     field.widget.attrs["class"] = "input is-size-6"


class BalanceSheetForm(forms.Form):
    """ 貸借対照表の期 """
    ki = forms.IntegerField(label='期')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input is-size-7"
