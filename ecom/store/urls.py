from django.urls import path
from . import views
urlpatterns = [
   path('', views.home, name = 'home'),
   path('about/', views.about, name = 'about'),
   path('login/', views.login_view, name = 'login'),
   path('register/', views.register, name = 'register'),
   path('logout/', views.logout_view, name = 'logout'),
   path('product/<int:pk>/', views.product, name='product'),
   path('category/<str:comm>', views.category, name = 'category'),

]