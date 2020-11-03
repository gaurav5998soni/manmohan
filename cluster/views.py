from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Article
from .forms import ArticleForm, ProductForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.

def home(request):
	mydict = {
		"Articles": Article.objects.all().order_by('-a_date')[:4],
		"Products": Product.objects.all()[:4]
	}
	return render(request, 'cluster/index.html',mydict)


def product(request):
	products = Product.objects.all()
	return render(request, 'cluster/products.html',{'products':products})


def product_detail(request, pk):
	context = {}
	context["product"] = Product.objects.get(id=pk)
	return render(request, 'cluster/product.html', context)


def delete_product(request, pk):
	obj = get_object_or_404(Product, id=pk)
	if request.user.is_authenticated:
		obj.delete()
		return redirect('products')
	return redirect('products')


def article(request):
	articles = Article.objects.all().order_by('-a_date')
	return render(request, 'cluster/articles.html',{'articles':articles})


def article_detail(request, pk):
	context = {}
	context["article"] = get_object_or_404(Article, id=pk)
	return render(request, 'cluster/article.html', context)


def delete_article(request, pk):
	obj = get_object_or_404(Article, id=pk)
	if request.user.is_authenticated:
		obj.delete()
		return redirect('articles')
	return redirect('articles')


def login_view(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request,
							username=username,
							password=password)
		if user is not None:
			
			login(request,user)
			messages.success(request, 'Login successfully!')

			return redirect('updates')
		else:
			messages.error(request, 'Username/Password is not valid!')

	return render(request, 'cluster/login.html')


def updates(request):
	a_form = ArticleForm()
	p_form = ProductForm()
	if request.method == "POST":
		a_form = ArticleForm(request.POST)
		if a_form.is_valid():
			title = a_form.cleaned_data.get('a_title')
			messages.success(request, 'Article {title} is created successfully!')
			a_form.save()
			return redirect('updates')
		else:
			p_form = ProductForm(request.POST, request.FILES)
			if p_form.is_valid():
				p_form.save()
				title = a_form.cleaned_data.get('p_title')
				messages.success(request, 'Article {title} is created successfully!')
				return redirect('updates')

	return render(request, 'cluster/updates.html')