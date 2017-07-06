from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm
from rango.forms import PageForm


def index(request):
    #B toShowIndex = "Rango says, <br> <h1>hello world !<h1>"+'<br><a href="/rango/about"> About </a>'
    #B return HttpResponse(toShowIndex)
    category_list = Category.objects.order_by('-likes')[:5]
    category_list2 = Category.objects.order_by('-views')[:5]
    context_dict = {'boldmessage':"Crunchy , Creamy , Cookie , Candy , CupCake !!!",'categories':category_list,'categories2':category_list2}

    return render(request,'rango/index.html',context=context_dict)


def about(request):
    # toShowAbout = "Rango says, <br> <h1>here is about this page !!!<h1>"+'<br><a href="/rango"> Main page </a>'
    # return HttpResponse(toShowAbout)
    context_dict1 = {'message':"yoo bro working super fine.."}
    return render(request,'rango/about.html',context=context_dict1)

def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug= category_name_slug)
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request,'rango/category.html',context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
