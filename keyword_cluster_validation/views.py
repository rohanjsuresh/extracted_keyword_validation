from django.shortcuts import render

# Create your views here.
def cluster_validation(request):
    return render(request, 'keyword_cluster_validation/visualization.html', {})