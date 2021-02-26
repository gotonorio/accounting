from django.contrib import admin
from .models import Master_category, Master_expense, Kanrihi_expense


# Register your models here.
class Master_categoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name',)


admin.site.register(Master_category, Master_categoryAdmin)


class Master_expenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'category', 'name', 'sequense')


admin.site.register(Master_expense, Master_expenseAdmin)


class Kanrihi_expenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'ki', 'master', 'expense')


admin.site.register(Kanrihi_expense, Kanrihi_expenseAdmin)
