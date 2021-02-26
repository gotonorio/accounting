from django.contrib import admin
from shuuzenhi_in.models import Master_shuuzenhi_income, Shuuzenhi_income


# Register your models here.
class Master_shuuzenhi_incomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')


admin.site.register(Master_shuuzenhi_income, Master_shuuzenhi_incomeAdmin)


class Shuuzenhi_incomeAdmin(admin.ModelAdmin):
    list_display = ('ki', 'master', 'income')


admin.site.register(Shuuzenhi_income, Shuuzenhi_incomeAdmin)
