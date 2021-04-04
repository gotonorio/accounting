from django.contrib import admin
from asset_list.models import Master_assetlist, AssetList, AccountType


class Master_assetlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'account_number',
                    'isAsset', 'sequense', 'alive', 'comment')


class AssetListAdmin(admin.ModelAdmin):
    list_display = ('id', 'ki', 'master', 'asset', 'comment')


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Master_assetlist, Master_assetlistAdmin)
admin.site.register(AssetList, AssetListAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
