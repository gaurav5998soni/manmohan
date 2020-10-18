from django.db import models
from PIL import Image
# Create your models here.
class Post(models.Model):
    title       = models.CharField(max_length=120)
    description = models.TextField()
    date        = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    title       = models.CharField(max_length=50)
    description = models.TextField()
    product_img = models.ImageField(upload_to="product_images")

    def save(self):
        super().save()

        img = Image.open(self.product_img.path)
        output_size = (500,500)
        img.thumbnail(output_size)
        img.save(self.product_img.path)

    def __str__(self):
        return self.title