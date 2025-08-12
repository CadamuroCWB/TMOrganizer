from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

# main views
def about(request):
    context = {
        'title': 'Techno Mania - About',
        'message': 'Solutions for the tech enthusiast. Smart solutions for a tech-savvy world',
        'description': 'Welcome to Techno Mania, your go-to source for the latest in technology, offering insights and solutions for tech enthusiasts. Explore the latest in technology with Techno Mania.',
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'about.html', context)

def contactus(request):
    context = {
        'title': 'Techno Mania - Contact Us',
        'message': 'Use the form below to get in touch with us.',
        'description': 'We are at your disposal to answer your questions and better serve you.',
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'contactus.html', context)

def index(request):
    context = {
        'title': 'Techno Mania - Home',
        'message': 'Escolha a linha de produtos que mais combina com você',
        'description': '',
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'is_superuser': request.user.is_superuser,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
    }
    return render(request, 'index.html', context)

# sale views
def item(request):
    context = {
        'title': 'Techno Mania - Item',
        'message': 'Os melhores produtos para você',
        'description': 'Explore nossa gama de produtos projetados para melhorar sua experiência tecnológica.',
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'item.html', context)

# error handlers
def custom_404_view(request, exception):
    context = {
        'title': 'Page Not Found',
        'message': 'The page you are looking for does not exist.',
        'description': '',
        'keywords': '',
    }
    return render(request, '404.html', context, status=404)

def custom_500_view(request):
    context = {
        'title': 'Server Error',
        'message': 'An unexpected error occurred.',
        'description': '',
        'keywords': '',
    }
    return render(request, '500.html', context, status=500)
