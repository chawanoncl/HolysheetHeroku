from django.contrib import admin
from .models import Author, Sheet, Page, UserLibrary

admin.site.register(Author)
admin.site.register(Sheet)
admin.site.register(Page)
admin.site.register(UserLibrary)