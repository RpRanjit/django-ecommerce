from django.urls import path
from . import views
urlpatterns = [
   path('', views.home, name = 'home'),
   path('about/', views.about, name = 'about'),
   path('login/', views.login_view, name = 'login'),
   path('register/', views.register, name = 'register'),
   path('user_update/', views.user_update, name = 'user_update'),
   path('update_password/', views.update_password, name = 'update_password'),
   path('update_info/', views.update_info, name = 'update_info'),
   path('logout/', views.logout_view, name = 'logout'),
   path('product/<int:pk>/', views.product, name='product'),
   path('category/<str:comm>', views.category, name = 'category'),
   path('category_summary', views.categroy_summary, name = 'category_summary'),
   path('search/', views.search, name = 'search'),

]