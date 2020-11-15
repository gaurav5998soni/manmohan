from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Article, ContactUs, OurTeam
from .forms import ArticleForm, ProductForm, ContactUsForm, OurTeamForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
# Create your views here.

def home(request):
	mydict = {
		"Articles": Article.objects.all().order_by('-a_date')[:3],
		"Products": Product.objects.all()[:4]
	}
	return render(request, 'cluster/index.html',mydict)



class Products(ListView):
	template_name = 'cluster/products.html'
	model = Product
	context_object_name = 'products'
	paginate_by = 12


def product_detail(request, pk):
	context = {}
	context["product"] = Product.objects.get(id=pk)
	return render(request, 'cluster/product.html', context)

class ProductUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Product
	fields = ['p_title','p_description', 'p_product_img']
	#
	# def form_valid(self, form):
	# 	form.instance.author = self.request.user
	# 	return super().form_valid(form)
	#
	def test_func(self):
		post = self.get_object()
		# if self.request.user == post.author:
		if self.request.user.is_authenticated:
			return True
		return False



class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Product
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user.is_authenticated:
			return True
		return False


class article(ListView):
	template_name = 'cluster/articles.html'
	model = Article
	context_object_name = 'articles'
	ordering = ['-a_date']
	paginate_by = 5



def article_detail(request, pk):
	context = {}
	context["article"] = get_object_or_404(Article, id=pk)
	return render(request, 'cluster/article.html', context)

class ArticleUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Article
	fields = ['a_title','a_description']

	def test_func(self):
		post = self.get_object()
		# if self.request.user == post.author:
		if self.request.user.is_authenticated:
			return True
		return False




class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Article
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user.is_authenticated:
			return True
		return False


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

	return render(request, 'cluster/admin/login.html')

def updates(request):
	a_form = ArticleForm()
	p_form = ProductForm()
	if request.method == "POST":
		a_form = ArticleForm(request.POST)
		p_form = ProductForm(request.POST, request.FILES)
		if a_form.is_valid():
			title = a_form.cleaned_data.get('a_title')
			messages.success(request, 'Article {title} is created successfully!')
			a_form.save()
			return redirect('updates')
		elif p_form.is_valid():
			p_form.save()
			title = a_form.cleaned_data.get('p_title')
			messages.success(request, 'Article {title} is created successfully!')
			return redirect('updates')
		else:
			messages.error(request, 'Username/Password is not valid!')

	return render(request, 'cluster/admin/updates.html')

def add_member(request):
	if request.method == "POST":
		form = OurTeamForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			messages.success(request, f'Hey {name}, is created successfully!')
			form.save()
			return redirect('our_team')
		else:
			messages.error(request, 'Fill all fields accurately!')

	return render(request, 'cluster/admin/add_member.html')

# def our_team(request):
# 	form = OurTeamForm()
# 	members = OurTeam.objects.all().order_by('-date')
# 	page    = request.GET.get('page', 1)
# 	paginator= Paginator(members, 10)
# 	try:
# 		users = paginator.page(page)
# 	except PageNotAnInteger:
# 		users = paginator(1)
# 	except EmptyPage:
# 		users = paginator.page(paginator.num_pages)
# 	context = {
# 		'members': members,
# 		'page_obj': users,
# 	}

# 	return render(request, 'cluster/admin/our_team.html', context)

def our_team(request):
	form = OurTeamForm()
	members = OurTeam.objects.all().order_by('-date')
	page    = request.GET.get('page', 1)
	paginator= Paginator(members, 10)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	
	query = request.GET.get('search')
	
	if query:
		members = OurTeam.objects.filter(Q(name__icontains=query)|
			Q(designation__icontains=query))
		
	context = {
		#'members': members,
		'page_obj': members,
	}
	
	return render(request, 'cluster/admin/our_team.html', context)



class OurTeamUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = OurTeam
	fields = '__all__'

	def test_func(self):
		post = self.get_object()
		# if self.request.user == post.author:
		if self.request.user.is_authenticated:
			return True
		return False

class OurTeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = OurTeam
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user.is_authenticated:
			return True
		return False



def searchMatch(query, member):
     # return true only if query match
     if query in member.name.lower() or query in member.designation.lower():
          return True
     else:
          return False

class SearchListView(ListView):
	model = OurTeam
	template_name = 'cluster/admin/search_our_team.html'
	paginate_by = 10

	def get(self, request):
		search = request.GET.get('search')
		print("search", search)
		members = OurTeam.objects.all()
		n_members = []
		for member in members:
			if searchMatch(search, member):
				n_members.append(member)
		print(n_members)
		return n_members



def contact_us(request):
	form = ContactUsForm()
	if request.method == "POST":
		form = ContactUsForm(request.POST)
		print(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			messages.success(request, f'{name}, is created!')
			form.save()
			return redirect('home')
		else:
			messages.error(request, 'Fill all fields accurately!')
	return render(request, 'cluster/contact_us.html', )

def contact_us_responses(request):
	responses = ContactUs.objects.all()
	return render(request, 'cluster/admin/contact_us_responses.html',{'responses':responses})


def support_us(request):
	return render(request, 'cluster/help_us.html')