from django.contrib import admin
from .models import Car

@admin.action(description='Mark selected cars as Sold')
def mark_as_sold(modeladmin, request, queryset):
    queryset.update(status='sold')

@admin.action(description='Mark selected cars as Repaired')
def mark_as_repaired(modeladmin, request, queryset):
    queryset.update(status='repaired')

@admin.action(description='Mark selected cars as Purchased')
def mark_as_purchased(modeladmin, request, queryset):
    queryset.update(status='purchased')

class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'status']
    list_filter = ['status']
    actions = [mark_as_sold, mark_as_repaired, mark_as_purchased]

admin.site.register(Car, CarAdmin)
