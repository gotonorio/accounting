from django.contrib import admin

from kanrihi_in.models import (Category_income, Kanrihi_income,
                               Master_kanrihi_income)


# Register your models here.
class Category_incomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')


admin.site.register(Category_income, Category_incomeAdmin)


class Master_kanrihi_incomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'category')


admin.site.register(Master_kanrihi_income, Master_kanrihi_incomeAdmin)


class Kanrihi_incomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ki', 'master', 'income')


admin.site.register(Kanrihi_income, Kanrihi_incomeAdmin)
