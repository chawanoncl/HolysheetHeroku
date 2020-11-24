from django.urls import path
from .views import sheet_preview

app_name = 'index'

urlpatterns = [
    path('', sheet_preview, name='sheet-preview'),
   
 
]