from django import forms
from django.db.models.aggregates import Max

from shuuzenhi_in.models import Master_shuuzenhi_income, Shuuzenhi_income
import logging


class Shuuzenhi_incomeForm(forms.ModelForm):
    """ models.pyのモデルを追加するためModelFormとする
    https://qiita.com/felyce/items/5042db0792c9f7d01c1e
    """
    max_ki = Shuuzenhi_income.objects.aggregate(ki=Max('ki'))
    if max_ki["ki"] is None:
        ki = forms.IntegerField(label='期', initial=0)
    else:
        ki = forms.IntegerField(label='期', initial=max_ki["ki"]+1)

    master = forms.ModelChoiceField(
        queryset=Master_shuuzenhi_income.objects.all(),
        label='収入種別'
    )
    income = forms.IntegerField(label='収入額')
    comment = forms.CharField(label='コメント', widget=forms.Textarea, required=False)

    def clean_master(self):
        """ validation """
        mn = self.cleaned_data['master']
        if mn.name == '駐車場収入':
            raise forms.ValidationError("駐車場収入は駐車場会計で処理してください")
        elif mn.name == '管理会計より繰入':
            raise forms.ValidationError("管理会計からの収入は管理会計で処理してください")
        return mn

    # 重複登録をチェックする。
    def clean(self):
        cleaned_data = super().clean()
        ki = cleaned_data['ki']
        master = cleaned_data['master']
        data = Shuuzenhi_income.objects.filter(ki=ki, master=master)
        if data:
            raise forms.ValidationError("既に登録済みです。")
        return cleaned_data

    class Meta:
        model = Shuuzenhi_income
        fields = ("ki", "master", "income", "comment")

    def __init__(self, *args, **kwargs):
        """ フォームフィールドにclassを設定 """
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input is-size-6"
        self.fields['master'].widget.attrs["class"] = "select-css is-size-6"
        self.fields['income'].widget.attrs["class"] = "input is-size-6"
        self.fields['comment'].widget.attrs["class"] = "textarea is-size-6"
        """
        for field in self.fields.values():
            field.widget.attrs["class"] = "select"
        """


class Shuuzenhi_masterForm(forms.ModelForm):
    """ 修繕費収入項目マスター """
    code = forms.IntegerField(label="コード")
    name = forms.CharField(label="収入項目名", max_length=256)
    alive = forms.BooleanField(label='有効', initial=True)

    class Meta:
        model = Master_shuuzenhi_income
        fields = ("code", "name", "alive")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs["class"] = "input is-size-6"
        self.fields['name'].widget.attrs["class"] = "input is-size-6"
        self.fields['alive'].widget.attrs["class"] = "checkbox is-size-6"
