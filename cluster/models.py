from django.db import models
from PIL import Image
# Create your models here.
class Article(models.Model):
    a_title       = models.CharField(max_length=120, null=False)
    a_description = models.TextField(null=False)
    a_date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.a_title

class Product(models.Model):
    p_title       = models.CharField(max_length=50, null=False)
    p_description = models.TextField(null=False)
    p_product_img = models.ImageField(upload_to="product_images", null=False)

    def save(self):
        super().save()

        img = Image.open(self.p_product_img.path)
        output_size = (300,300)
        img.thumbnail(output_size)
        img.save(self.p_product_img.path)

    def __str__(self):
        return self.p_title