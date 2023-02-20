from django.contrib import admin
from django.urls import path, re_path
from vine_app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.homepage, name="home"),
    path("", views.homepage, name="index"),
    path("wine/<int:wine_id>", views.show_wine, name="show_wine"),
    path("shelf/<int:id>", views.show_shelf, name="show_shelf"),
    path('login/', views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name="profile"),
    path("wine/create/", views.create_wine, name="wine_create"),
    path("wine/edit/<int:wine_id>", views.WineUpdateView.as_view(template_name='wine/wine_edit.html'), name="wine_edit"),
    path("wine/delete/<int:wine_id>", views.WineDeleteView.as_view(), name="wine_delete"),
    path("profile/wines", views.wine_list, name="wine_list"),
    path("profile/shelfs", views.shelf_list, name="shelfs_list"),
    path("profile/cabinets", views.cabinet_list, name="cabinet_list"),
    path("profile/clients", views.client_list, name="client_list"),
    path("shelf/create", views.ShelfCreateView.as_view(template_name="shelf/shelf_create.html"), name="shelf_create"),
    path("shelf/edit/<int:id>", views.ShelfUpdateView.as_view(template_name='shelf/shelf_edit.html'), name="shelf_edit"),
    path("shelf/delete/<int:id>", views.ShelfDeleteView.as_view(), name="shelf_delete"),
    path("cabinet/<int:id>", views.show_cabinet, name="cabinet_show"),
    path("cabinet/create", views.CabinetCreateView.as_view(template_name="cabinet/cabinet_create.html"), name = "cabinet_create"),
    path("cabinet/edit/<int:id>", views.CabinetUpdateView.as_view(template_name='cabinet/cabinet_edit.html'), name="cabinet_edit"),
    path("cabinet/delete/<int:id>", views.CabinetDeleteView.as_view(), name="cabinet_delete"),
    path("client/<int:id>", views.client_show, name="client_show"),
    path("client/create", views.client_create, name = "client_create"),
    path("client/edit/<int:id>", views.UserUpdateView.as_view(template_name='client/client_edit.html'), name="client_edit"),
    path("editable_cards/", views.editable_card_list, name="editable_card_list"),
    path("client/delete/<int:id>", views.UserDeleteView.as_view(), name="client_delete"),
    path("search", views.search, name="search"),
    path("download_example_doc/", views.download_file, name = "download_doc"),
    path("relogin/", views.relogin, name="relogin"),
    path("fastlink", views.fastlink, name="fastlink"),
    path("invalid_code", views.invalid_code, name="invalid_code"),
    path("valid_code", views.valid_code, name="valid_code"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
