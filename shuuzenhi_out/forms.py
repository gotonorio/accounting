from django import forms
from django.db.models.aggregates import Max
from django.conf import settings

# from file_storage.models import Category
from shuuzenhi_out.models import (Constractor, Master_koujitype, Shuuzenhi_expense)


class SelectClassForm(forms.Form):
    """ 履歴一覧表示の時にselect要素で工事種別を選択させる．
    http://www.subthread.co.jp/blog/20160531/
    """
    # querysetを使う場合はforms.ModelChoiceFiled()を使う。empty_labelを使用できる。
    kouji_type = forms.ModelChoiceField(
        queryset=Master_koujitype.objects.filter(live='1').order_by('sequense'),
        label='工事種別',
        empty_label='工事種別全表示',
        error_messages={
            'required': "You didn't select a choice.",
            'invalid_choice': "invalid choice.",
        },
        required=False,
        widget=forms.Select(attrs={'class': 'select-css is-size-6'})
    )
    year = forms.ModelChoiceField(
        # 修繕履歴データから西暦を抽出してセットする。
        queryset=Shuuzenhi_expense.objects.values_list(
            'year', flat=True).order_by('year').distinct(),
        label='西暦',
        empty_label='年度全表示',
        error_messages={
            'required': "You didn't select a choice.",
            'invalid_choice': "invalid choice.",
        },
        required=False,
        widget=forms.Select(attrs={'class': 'select-css is-size-6'})
    )
    accounting_type = [('ALL', '会計区分全表示'), ]
    accounting_type.extend(settings.ACCOUNTING_TYPE)
    account_type = forms.ChoiceField(
        choices=accounting_type,
        widget=forms.Select(attrs={'class': 'select-css is-size-6'})
    )


class Shuuzenhi_expenseForm(forms.ModelForm):
    """ 修繕費支出データの登録 """
    max_year = Shuuzenhi_expense.objects.aggregate(year=Max('year'))
    if max_year["year"] is None:
        year = 1999
    else:
        year = forms.IntegerField(label='西暦', initial=max_year["year"]+1)
    koujitype = forms.ModelChoiceField(
        queryset=Master_koujitype.objects.filter(live='1').order_by('sequense'),
        label='支出種別'
    )
    koujimei = forms.CharField(
        label='工事名', widget=forms.TextInput(attrs={'size': 32}))
    cost = forms.IntegerField(label='支出額')
    constractor = forms.ModelChoiceField(
        queryset=Constractor.objects.all().order_by('sequense'),
        label='施工業者'
    )
    quotation_id = forms.IntegerField(label='見積書ID', initial=0)
    comment = forms.CharField(
        label='コメント', widget=forms.Textarea, required=False)

    class Meta:
        model = Shuuzenhi_expense
        fields = ("year", "koujitype", "koujimei", "cost",
                  "constractor", "account_type", "quotation_id", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].widget.attrs["class"] = "input"
        self.fields['koujitype'].widget.attrs["class"] = "select-css"
        self.fields['koujimei'].widget.attrs["class"] = "input"
        self.fields['cost'].widget.attrs["class"] = "input"
        self.fields['constractor'].widget.attrs["class"] = "select-css"
        self.fields['account_type'].widget.attrs["class"] = "select-css"
        self.fields['quotation_id'].widget.attrs["class"] = "input"
        self.fields['comment'].widget.attrs["class"] = "textarea"
        self.fields['comment'].widget.attrs["rows"] = "4"


class Master_koujitypeForm(forms.ModelForm):
    """ 修繕費支出項目マスターの登録用フォーム """
    sequense = forms.IntegerField(label="表示順序")
    koujitype = forms.CharField(label="工事種別名", max_length=256)
    live = forms.IntegerField(label="有効/無効", initial=1)

    class Meta:
        model = Master_koujitype
        fields = ("sequense", "koujitype", "live")

    # fieldにclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sequense'].widget.attrs["class"] = "input is-size-6"
        self.fields['koujitype'].widget.attrs["class"] = "select-css is-size-6"
        self.fields['live'].widget.attrs["class"] = "input is-size-6"


class ConstractorForm(forms.ModelForm):
    """ 施工業者マスターの登録用フォーム """
    sequense = forms.IntegerField(label="表示順序")
    name = forms.CharField(label="施工業者", max_length=128)
    comment = forms.CharField(
        label='コメント', widget=forms.Textarea, required=False)

    class Meta:
        model = Constractor
        fields = ("sequense", "name", "comment")

    # fieldにclassを設定する。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sequense'].widget.attrs["class"] = "input is-size-6"
        self.fields['name'].widget.attrs["class"] = "input is-size-6"
        self.fields['comment'].widget.attrs["class"] = "text is-size-6"

        """
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        """


#class QuotationForm(forms.Form):
#    """ 見積書一覧用Form """
#    category = forms.ModelChoiceField(
#        queryset=Category.objects.order_by('-created_at'),
#        label='工事種別',
#        empty_label='工事種別全表示',
#        error_messages={
#            'required': "You didn't select a choice.",
#            'invalid_choice': "invalid choice.",
#        },
#        required=False,
#        initial=None,
#        widget=forms.Select(attrs={'class': 'select-css is-size-7'})
#    )
