from django import forms
from .models import Article, Product

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

