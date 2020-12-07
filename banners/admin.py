from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from banners.models import Banner


@admin.register(Banner)
class BannerAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
    #this doesnt save order. no idea why
