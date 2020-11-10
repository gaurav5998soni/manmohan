from django import forms
from .models import Article, Product, ContactUs, OurTeam

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'

class OurTeamForm(forms.ModelForm):
    class Meta:
        model = OurTeam
        fields = '__all__'
