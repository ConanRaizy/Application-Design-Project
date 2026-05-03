from django.contrib import admin
from .models import Car, Review

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'year', 'price', 'status', 'created_at']
    list_filter = ['status', 'fuel_type']
    search_fields = ['make', 'model']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'title', 'rating', 'is_approved', 'submitted_at']
    list_filter = ['is_approved', 'rating']
    search_fields = ['customer_name', 'title']
