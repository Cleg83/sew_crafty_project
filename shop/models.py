from django.db import models

# Create your models here.
class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=300)
    display_name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_display_name(self):
        return self.display_name
    

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=False, blank=False, default='no-image.svg')
    in_stock = models.BooleanField(default=True, null=True, blank=True)
    permanently_unavailable = models.BooleanField(default=False, help_text="Mark this product as unavailable for sale.")

    def __str__(self):
        return self.name
    


