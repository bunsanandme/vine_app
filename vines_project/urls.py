from django.contrib import admin
from django.urls import path
from vine_app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.homepage, name="home"),
    path("wine/<int:wine_id>", views.show_wine, name="show_wine"),
    path("shelf/<int:id>", views.show_shelf, name="show_shelf"),
    path("register/", views.register, name="register"),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name="profile"),
    path("wine/create/", views.create_wine, name="wine_create"),
    path("wine/edit/<int:wine_id>", views.WineUpdateView.as_view(template_name='wine_edit.html'), name="wine_edit"),
    path("wine/delete/<int:wine_id>", views.WineDeleteView.as_view(), name="wine_delete"),
    path("profile/wines", views.wine_list, name="wine_list"),
    path("profile/editable_wines", views.editable_wine_list, name="editable_wine_list"),
    path("profile/shelfs", views.shelf_list, name="shelfs_list"),
    path("shelf/create", views.ShelfCreateView.as_view(template_name="shelf_create.html"), name = "shelf_create"),
    path("shelf/edit/<int:id>", views.ShelfUpdateView.as_view(template_name='shelf_edit.html'), name="shelf_edit"),
    path("shelf/delete/<int:id>", views.ShelfDeleteView.as_view(), name="shelf_delete"),
    path("search", views.search, name="search"),
    path("download_example_doc/", views.download_file, name = "download_doc"),
    path("relogin/", views.relogin, name="relogin"),
    path("test/", views.test, name="test")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
