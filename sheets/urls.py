from django.urls import path
from .views import sheet_list, sheet_detail, page_detail

app_name = 'sheets'

urlpatterns = [
    path('', sheet_list, name='sheet-list'),
    path('<slug>/', sheet_detail, name='sheet-detail'),
    path('<sheet_slug>/<int:page_number>', page_detail, name='page-detail')
 
]