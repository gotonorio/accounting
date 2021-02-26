from django.contrib import admin
from asset_list.models import Master_assetlist, AssetList


class Master_assetlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'account_number',
                    'isAsset', 'sequense', 'alive', 'comment')


class AssetListAdmin(admin.ModelAdmin):
    list_display = ('id', 'ki', 'master', 'asset', 'comment')


admin.site.register(Master_assetlist, Master_assetlistAdmin)
admin.site.register(AssetList, AssetListAdmin)
