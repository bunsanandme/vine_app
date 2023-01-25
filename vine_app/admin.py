from django.contrib import admin
from vine_app.models import Wine, Shelf
from django.contrib.auth.models import User, Group

admin.site.register(Wine)
admin.site.register(Shelf)

