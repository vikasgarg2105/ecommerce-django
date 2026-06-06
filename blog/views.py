from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def bloghome(request):
    return render(request, 'blog/index.html')