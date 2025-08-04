from django.contrib import admin
from .models import Car, User

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
    list_display = ['id','name', 'price', 'status']
    list_filter = ['status']
    actions = [mark_as_sold, mark_as_repaired, mark_as_purchased]

admin.site.register(Car, CarAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email', 'first_name', 'is_active']
admin.site.register(User,UserAdmin)
