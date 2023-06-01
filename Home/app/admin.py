from django.contrib import admin

# import models  
from .models import *

# Register your models here.

class Product_Images(admin.TabularInline):
    model = Product_Image

class Aditional_Informations(admin.TabularInline):
    model = Aditional_Information

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images,Aditional_Informations)
    list_display = ('Products_name','Price','Categorys','section')
    list_editable = ('Categorys', 'section')


admin.site.register(Section)
admin.site.register(Product, Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Aditional_Information)

admin.site.register(slider)
admin.site.register(banner)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Coupon_Code)


