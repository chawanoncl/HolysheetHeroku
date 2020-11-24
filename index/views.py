from django.shortcuts import render
from sheets.models import Sheet

def index_view(request):
    
    return render(request, "index.html")

def sheet_preview(request):
    queryset = Sheet.objects.all()
    context = {
        'queryset': queryset
    }
    return render(request, "index.html", context)