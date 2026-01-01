
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Importe as views prontas do Django
from banco import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('banco/', include('banco.app_urls')),

    # Rota de Login e Logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('bankgo/', views.entrance, name='entrance'),

]




