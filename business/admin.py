from django.contrib import admin
from .models import Location, Suburb, Category, Business, Menu, Reviews, Reservations, Promotion, Images, Claim
	
class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}
	
admin.site.register(Location, LocationAdmin)

class SuburbAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}
	
admin.site.register(Suburb, SuburbAdmin)

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class BusinessAdmin(admin.ModelAdmin):
	list_display = ['location', 'suburb', 'category', 'name', 'description', 'slug']
	prepopulated_fields = {'slug': ('name',)}

class PromotionAdmin(admin.ModelAdmin):
	list_display = ['business', 'name', 'number_of_reservations', 'description', 'startDate', 'endDate']
	prepopulated_fields = {'slug': ('name',)}


admin.site.register(Claim)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Menu)
admin.site.register(Reviews)
admin.site.register(Reservations)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Images)

