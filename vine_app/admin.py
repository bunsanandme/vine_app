from django.contrib import admin
from vine_app.models import Wine, Shelf, Cabinet
from django.contrib.auth.models import User, Group

class Admin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Wine)
admin.site.register(Shelf)
admin.site.register(Cabinet)
