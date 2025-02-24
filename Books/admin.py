from django.contrib import admin
from . import models
from .models import Borrow


admin.site.register(models.Books)

class Categoryadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

admin.site.register(models.Category, Categoryadmin)
admin.site.register(models.Comment)


class BorrowAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "timestamp", "status")  # timestamp যুক্ত আছে
    readonly_fields = ("timestamp",)

admin.site.register(Borrow, BorrowAdmin)  # ✅ শুধুমাত্র এই রেজিস্ট্রেশন রাখুন
