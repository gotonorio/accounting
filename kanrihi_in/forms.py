# import logging
from datetime import datetime

from django import forms
from django.conf import settings

# from django.db.models.aggregates import Max
from kanrihi_in.models import (Category_income, Kanrihi_income,
                               Master_kanrihi_income)


class Kanrihi_incomeForm(forms.ModelForm):
    """ models.pyのモデルを追加するためModelFormとする
    https://qiita.com/felyce/items/5042db0792c9f7d01c1e
    """
    # 新しく登録する「期」をデフォルト表示するため。
    this_ki = datetime.now().year - settings.START_YEAR - 1
    ki = forms.IntegerField(label='期', initial=this_ki)
    """
    max_ki = Kanrihi_income.objects.aggregate(ki=Max('ki'))
    if max_ki["ki"] is None:
        ki = forms.IntegerField(label='期', initial=0)
    else:
        ki = forms.IntegerField(label='期', initial=max_ki["ki"]+1)
    """
    # 以下はtemplatesでformフィールド名を表示させるため。無くても表示がmodelsの要素名になるだけ。
    master = forms.ModelChoiceField(
        queryset=Master_kanrihi_income.objects.all(),
        label='収入種別'
    )
    income = forms.IntegerField(label='収入額')

    def clean_master(self):
        """ validation """
        mn = self.cleaned_data['master']
        if mn.name == '駐車場収入':
            raise forms.ValidationError("駐車場収入は駐車場会計で処理してください")
        return mn

    # 重複登録をチェックする。
    def clean(self):
        cleaned_data = super().clean()
        ki = cleaned_data['ki']
        master = cleaned_data['master']
        data = Kanrihi_income.objects.filter(ki=ki, master=master)
        if data:
            raise forms.ValidationError("既に登録済みです。")
        return cleaned_data

    # インナークラスでmodel、fieldを指定する。（これでモデルに紐づける）
    # （https://djangogirlsjapan.gitbooks.io/workshop_tutorialjp/content/django_forms/）
    class Meta:
        model = Kanrihi_income
        fields = ("ki", "master", "income")

    # fieldにbootstrap4用のclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input is-size-6"
        self.fields['master'].widget.attrs["class"] = "select-css is-size-6"
        self.fields['income'].widget.attrs["class"] = "input is-size-6"
        """
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        """


class Kanrihi_masterForm(forms.ModelForm):
    """ 管理費収入項目マスター作成用Form """
    code = forms.IntegerField(label="コード")
    name = forms.CharField(label="収入項目名", max_length=256)

    class Meta:
        model = Master_kanrihi_income
        fields = ("code", "name", "category")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs["class"] = "input is-size-6"
        self.fields['name'].widget.attrs["class"] = "input is-size-6"
        self.fields['category'].widget.attrs["class"] = "select-css is-size-6"


class Master_categoryForm(forms.ModelForm):
    """ 管理費収入カテゴリーの登録用フォーム """
    name = forms.CharField(
        label="収入カテゴリ名",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'input is-size-6'})
        )

    class Meta:
        model = Category_income
        fields = ("code", "name",)

    # fieldにclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs["class"] = "input is-size-6"
