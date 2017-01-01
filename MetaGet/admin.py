from django.contrib import admin

# Register your models here.
from MetaGet.models import WebSite, Image


def scan_WebSite(modeladmin, request, queryset):
    for obj in queryset:
        obj.scan()

class WebSiteAdmin(admin.ModelAdmin):
    list_display = ['Url', 'LastScan', 'ContentType']
    list_filter = ['LastScan', 'Scanned', 'ContentType']
    # fields to search in change list
    search_fields = ['Url', 'MD5Sum']
    readonly_fields = ('Scanned', 'LastScan', 'MD5Sum', 'encoding', 'ContentType', 'Cookies')
    # enable the save buttons on top on change form
    save_on_top = True
    actions = [scan_WebSite]

class ImageAdmin(admin.ModelAdmin):
    list_filter = ['HasEXIF', 'CamModel']
    readonly_fields = ('Url', 'Bild', 'HasEXIF', 'CamModel', 'DateTimeDigitized', 'MD5sum', 'ExifImageHeight', 'ExifImageWidth')
    
    
admin.site.register(WebSite, WebSiteAdmin)
admin.site.register(Image, ImageAdmin)

