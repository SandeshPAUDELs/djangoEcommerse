from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, FormView

from ecomapp1.models import Product

@login_required(login_url='loginPage')
def index(request):
    product_list = Product.objects.all()
    return render(request, 'index.html', {'product_list': product_list})


# def search(request):
#     product_list = Product.objects.filter(title__icontains=request.GET['title'])
#     return render(request, 'index.html', {'product_list': product_list})
def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        results = Product.objects.filter(title__icontains=keyword)
        return render(request, 'search.html', {'results': results})