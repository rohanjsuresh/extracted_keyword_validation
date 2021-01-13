from django.shortcuts import render
from .models import Keyword_Pages

# Create your views here.

def home(request):
    return render(request, 'keyword_relation/index.html', {})

def keyword_pages(request):
    return render(request, 'keyword_relation/keyword_pages_default.html', {})

def dynamic_lookup_view(request, keyword):
    obj = Keyword_Pages.objects.get(keyword=keyword)
    context = {
        "keyword":obj.keyword.capitalize(),
        "matched":obj.matched_with,
    }
    return render(request, 'keyword_relation/keyword_page.html', context)

def search(request):
    search_input = request.POST.get("search_input")
    return dynamic_lookup_view(request, search_input)