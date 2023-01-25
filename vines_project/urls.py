from django.contrib import admin
from django.urls import path
from vine_app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.homepage, name="home"),
    path("wine/<int:wine_id>", views.show_wine, name="show_wine"),
    path("shelf/<int:shelf_id>", views.show_shelf, name="show_shelf"),
    path("register/", views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', views.profile, name="profile"),
    path("wine/create/", views.create_wine, name="wine_create"),
    path("wine/edit/<int:wine_id>", views.WineUpdateView.as_view(template_name='wine_edit.html'), name="wine_edit"),
    path("wine/delete/<int:wine_id>", views.WineDeleteView.as_view(template_name='wine_delete.html'), name="wine_delete"),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
