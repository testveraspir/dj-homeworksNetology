from django.contrib import admin
from .models import Phone


class PhoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image',
                    'release_date', 'lte_exists', 'slug']
    list_filter = ['name', 'price']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Phone, PhoneAdmin)
