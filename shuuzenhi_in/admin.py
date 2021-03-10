from django.contrib import admin
from shuuzenhi_in.models import Master_shuuzenhi_income, Shuuzenhi_income, Category_shuuzenhi_income


# Register your models here.
class Category_shuuzenhi_incomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')


admin.site.register(Category_shuuzenhi_income, Category_shuuzenhi_incomeAdmin)


class Master_shuuzenhi_incomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'category')


admin.site.register(Master_shuuzenhi_income, Master_shuuzenhi_incomeAdmin)


class Shuuzenhi_incomeAdmin(admin.ModelAdmin):
    list_display = ('ki', 'master', 'income')


admin.site.register(Shuuzenhi_income, Shuuzenhi_incomeAdmin)
