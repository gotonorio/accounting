# Register your models here.
from django.contrib import admin
from shuuzenhi_out.models import (Constractor, Master_koujitype, Shuuzenhi_expense)


class Master_koujitypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'koujitype', 'sequense', 'live')


admin.site.register(Master_koujitype, Master_koujitypeAdmin)


class ConstractorAdmin(admin.ModelAdmin):
    list_display = ('id', 'sequense', 'name', 'comment')


admin.site.register(Constractor, ConstractorAdmin)


class Shuuzenhi_expenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'koujitype', 'koujimei',
                    'cost', 'constractor', 'account_type', 'comment')


admin.site.register(Shuuzenhi_expense, Shuuzenhi_expenseAdmin)
