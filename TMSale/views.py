from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render

@login_required
def contact(request):
    context = {
        'title': 'Techno Mania - Contato',
        'msg_title': 'Cadastrar contatos',
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'contact_list.html', context)
