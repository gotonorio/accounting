from django import forms
from .models import Account_subject, ExpenseItem


MONTH = (
    ('0', 'ALL'),
    ('1', '1月'),
    ('2', '2月'),
    ('3', '3月'),
    ('4', '4月'),
    ('5', '5月'),
    ('6', '6月'),
    ('7', '7月'),
    ('8', '8月'),
    ('9', '9月'),
    ('10', '10月'),
    ('11', '11月'),
    ('12', '12月')
)


class ExpenditureForm(forms.ModelForm):
    """ 小口会計データ入力用Form """
    expense_item = forms.ModelChoiceField(
        label='費目',
        queryset=ExpenseItem.objects.all(),
    )

    class Meta:
        model = Account_subject
        fields = ['spending_date', 'name', 'expense_item', 'expense', 'comment']

    def __init__(self, *args, **kwargs):
        super(ExpenditureForm, self).__init__(*args, **kwargs)
        self.fields['spending_date'].widget.attrs["class"] = "input"
        self.fields['name'].widget.attrs["class"] = "input"
        self.fields['expense_item'].widget.attrs["class"] = "select-css"
        self.fields['expense'].widget.attrs["class"] = "input"
        self.fields['comment'].widget.attrs["class"] = "textarea"
        self.fields['comment'].widget.attrs["rows"] = "4"


class AccountSubjectListForm(forms.Form):
    """ データ選択用Form """
    year = forms.IntegerField(label='西暦',)
    month = forms.ChoiceField(
        label='月',
        choices=MONTH,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].widget.attrs["class"] = "input is-size-7"
        self.fields['month'].widget.attrs["class"] = "select-css is-size-7"
