import logging
from datetime import datetime

from django import forms
from django.conf import settings

# from django.db.models.aggregates import Max
from kanrihi_out.models import Kanrihi_expense, Master_category, Master_expense


class Kanrihi_expenseForm(forms.ModelForm):
    """ 管理会計の支出登録用フォーム """
    # デフォルトの値（期）を求めておく。
    this_ki = datetime.now().year - settings.START_YEAR - 1
    ki = forms.IntegerField(label='期', initial=this_ki)

    # インナークラスでmodel、fieldを指定する。
    # （https://djangogirlsjapan.gitbooks.io/workshop_tutorialjp/content/django_forms/）
    class Meta:
        model = Kanrihi_expense
        fields = ("ki", "master", "expense")
        labels = {
            'master': '支出種別',
            'expense': '支出額'
        }

    # fieldにclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input"
        self.fields['master'].widget.attrs["class"] = "select-css"
        self.fields['expense'].widget.attrs["class"] = "input"

    """
    # 重複登録をチェックするためのvalidate。 ユニーク制約でチェックする
    # models.pyで複数項目のユニーク属性の方がスマート。
    def clean(self):
        cleaned_data = super().clean()
        ki = cleaned_data['ki']
        master = cleaned_data['master']
        data = Kanrihi_expense.objects.filter(ki=ki, master=master)
        if data:
            raise forms.ValidationError("既に登録済みです。")
        return cleaned_data
    """


class Master_expenseForm(forms.ModelForm):
    """ 管理費支出項目マスターの登録用フォーム """
    sequense = forms.IntegerField(label='表示順', initial=0)
    name = forms.CharField(label="支出項目名", max_length=256)
    category = forms.ModelChoiceField(
        queryset=Master_category.objects.all(),
        label='カテゴリー'
    )

    class Meta:
        model = Master_expense
        fields = ("code", "sequense", "name", "category")

    # fieldにclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs["class"] = "input"
        self.fields['sequense'].widget.attrs["class"] = "input"
        self.fields['name'].widget.attrs["class"] = "input"
        self.fields['category'].widget.attrs["class"] = "select-css"
        """
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        """


class Master_categoryForm(forms.ModelForm):
    """ 管理費支出カテゴリーの登録用フォーム """
    name = forms.CharField(
        label="支出カテゴリ名",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'input'})
        )

    class Meta:
        model = Master_category
        fields = ("code", "name",)

    # fieldにclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs["class"] = "input"


class CSVimportForm(forms.Form):
    """ 管理費支出データのインポート用フォーム """
    file = forms.FileField(
        label='CSVファイル', help_text='CSVデータ構造： id(pk), ki, Master_expenseのid(pk), expense')

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.name.endswith('.csv'):
            return file
        else:
            raise forms.ValidationError('拡張子がcsvのファイルをアップロードしてください')
