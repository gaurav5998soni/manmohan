from django.contrib import admin
from .models import Article, Product, ContactUs, OurTeam
# Register your models here.
admin.site.register(Article)
admin.site.register(Product)
admin.site.register(ContactUs)
admin.site.register(OurTeam)