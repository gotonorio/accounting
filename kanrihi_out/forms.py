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
    """
    max_ki = Kanrihi_expense.objects.aggregate(ki=Max('ki'))
    if max_ki["ki"] is None:
        ki = forms.IntegerField(label='期', initial=0)
    else:
        ki = forms.IntegerField(label='期', initial=max_ki["ki"])
    """
    master = forms.ModelChoiceField(
        queryset=Master_expense.objects.all(),
        label='支出種別'
    )
    expense = forms.IntegerField(label='支出額')

    # インナークラスでmodel、fieldを指定する。
    # （https://djangogirlsjapan.gitbooks.io/workshop_tutorialjp/content/django_forms/）
    class Meta:
        model = Kanrihi_expense
        fields = ("ki", "master", "expense")

    # fieldにclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ki'].widget.attrs["class"] = "input is-size-6"
        self.fields['master'].widget.attrs["class"] = "select-css is-size-6"
        self.fields['expense'].widget.attrs["class"] = "input is-size-6"


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
        fields = ("sequense", "name", "category")

    # fieldにclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sequense'].widget.attrs["class"] = "input is-size-6"
        self.fields['name'].widget.attrs["class"] = "input is-size-6"
        self.fields['category'].widget.attrs["class"] = "select-css is-size-6"
        """
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        """


class Master_categoryForm(forms.ModelForm):
    """ 管理費支出カテゴリーの登録用フォーム """
    name = forms.CharField(
        label="支出カテゴリ名",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'input is-size-6'})
        )

    class Meta:
        model = Master_category
        fields = ("code", "name",)

    # fieldにclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs["class"] = "input is-size-6"


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
