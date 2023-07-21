from django.contrib import admin
from .models import Artist, Artwork, Order, Type, Basic
# Register your models here.

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
	list_display = ('name',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
	list_display = ('name', 'types', 'date')
	list_filter = ('types',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('client', 'pk', 'state', 'types', 'date', 'amount')
	list_filter = ('state', 'types')

@admin.register(Basic)
class BasicAdmin(admin.ModelAdmin):
	list_display = ('title', )