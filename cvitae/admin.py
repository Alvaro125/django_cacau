from django.contrib import admin

from cvitae.models import CVitae


# Register your models here.
@admin.register(CVitae)
class CVitaeAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'content', 'created')
    search_fields = ('profile__user__username', 'content')