from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.product, name="products"),
    path('products/<int:pk>/', views.single_product, name="product"),
    path('products/<int:pk>/delete/', views.delete_product, name="delete_product"),
    path('articles/', views.article, name="articles"),
    path('article/<int:pk>/', views.single_article, name="article"),
    path('article/<int:pk>/delete/', views.delete_article, name="delete_article"),
    path('updates/', views.updates, name="updates"),
    path('login/',views.login_view, name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='cluster/logout.html'), name="logout")
]
