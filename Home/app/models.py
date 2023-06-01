from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save



# Create your models here.

class slider(models.Model):

    DISCOUNT_DEAL = (
        ('HOT DEALS', 'HOT DEALS'),
        ('New Arrivals', 'New Arrivals'),
    )

    Image = models.ImageField(upload_to='media/slider_image')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL, max_length=200)
    Sale = models.IntegerField()
    Brand_Name = models.CharField(max_length=200)
    Discout = models.IntegerField()
    Link = models.CharField(max_length=200)

    def __str__(self):
        return self.Brand_Name
    
class banner(models.Model):
    Image = models.ImageField(upload_to='media/banner_img')
    Discount_Deal = models.CharField(max_length=200)
    Quote = models.CharField(max_length=100)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.Quote
    
    
class Main_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " -- " +self.main_category.name
    
    
class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.category.main_category.name + " -- " + self.category.name + " -- " + self.name
    


class Section(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Color(models.Model):
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    Total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    Featured_image = models.CharField(max_length=200)
    Products_name = models.CharField(max_length=200)
    Brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    Price = models.IntegerField()
    Discount = models.IntegerField()
    tax = models.IntegerField(null=True)
    packing_cost = models.IntegerField(null=True)
    Product_information = RichTextField(null=True)
    Model_Name = models.CharField(max_length=200)
    Categorys = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    Tags = models.CharField(max_length=100)
    Description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)


    def __str__(self):
        return self.Products_name
    

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.Products_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)

    
class Coupon_Code(models.Model):
    code = models.CharField(max_length=100)
    discount = models.IntegerField()

    def __str__(self):
        return self.code


class Product_Image(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Image_url = models.CharField(max_length=200)

class Aditional_Information(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)
