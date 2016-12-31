from django.contrib import admin

# Register your models here.
from MetaGet.models import WebSite

def scan_WebSite(modeladmin, request, queryset):
    for obj in queryset:
        obj.scan()

class WebSiteAdmin(admin.ModelAdmin):
    list_display = ['Url', 'LastScan']
    list_filter = ['LastScan', 'Scanned']
    # fields to search in change list
    search_fields = ['Url', 'MD5Sum']
    # enable the save buttons on top on change form
    save_on_top = True
    actions = [scan_WebSite]
    
admin.site.register(WebSite, WebSiteAdmin)
