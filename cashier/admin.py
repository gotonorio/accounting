from django.contrib import admin
from .models import Account_subject, ExpenseItem


# Register your models here.
class Account_subjectAdmin(admin.ModelAdmin):
    list_display = ('spending_date', 'name', 'expense_item',
                    'expense', 'comment')


class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = ('item', )


admin.site.register(Account_subject, Account_subjectAdmin)
admin.site.register(ExpenseItem, ExpenseItemAdmin)
