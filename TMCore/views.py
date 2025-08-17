from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ContactUsForm

# main views
def about(request):
    context = {
        'title': 'Techno Mania - About',
        'msg_title': 'Solutions for the tech enthusiast. Smart solutions for a tech-savvy world',
        'description': 'Welcome to Techno Mania, your go-to source for the latest in technology, offering insights and solutions for tech enthusiasts. Explore the latest in technology with Techno Mania.',
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'about.html', context)

def contact(request):
    context = {
        'title': 'Techno Mania - Contact',
        'msg_title': 'Register prospective customers and suppliers',
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'contact.html', context)

def contactus(request):
    form = ContactUsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.send_mail()
            except Exception as e:
                messages.error = (request, f"Ocorreu um erro ao enviar sua mensagem: {e}")
            messages.success = (request, "Obrigado por entrar em contato conosco. Responderemos o mais breve possível.")
            #form = ContactUsForm()  # Reset the form after submission
        else:
            messages.error = (request, "Por favor, preencha o formulário abaixo para entrar em contato conosco.")
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    context = {
        'form': form,
        'title': 'Techno Mania - Contact Us',
        'msg_title': 'Utilize o formulário abaixo para entrar em contato conosco',
        'description': 'We are at your disposal to answer your questions and better serve you.',
        'user': user,
        'is_authenticated': request.user.is_authenticated,
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'contactus.html', context)

def index(request):
    context = {
        'title': 'Techno Mania - Home',
        'msg_title': 'Escolha a linha de produtos que mais combina com você',
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
        'msg_title': 'Os melhores produtos para você',
        'description': 'Explore nossa gama de produtos projetados para melhorar sua experiência tecnológica.',
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'item.html', context)

# error handlers
def custom_404_view(request, exception):
    context = {
        'title': 'Page Not Found',
        'msg_title': 'The page you are looking for does not exist.',
        'description': '',
        'keywords': '',
    }
    return render(request, '404.html', context, status=404)

def custom_500_view(request):
    context = {
        'title': 'Server Error',
        'msg_title': 'An unexpected error occurred.',
        'description': '',
        'keywords': '',
    }
    return render(request, '500.html', context, status=500)
