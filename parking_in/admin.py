from django.contrib import admin
from parking_in.models import Master_parking_income


class Master_parking_incomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')


admin.site.register(Master_parking_income, Master_parking_incomeAdmin)
