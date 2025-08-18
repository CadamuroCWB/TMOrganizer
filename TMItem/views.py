from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render

@login_required
def item(request):
    context = {
        'title': 'Techno Mania - Item',
        'msg_title': 'Os melhores produtos para você',
        'description': 'Explore nossa gama de produtos projetados para melhorar sua experiência tecnológica.',
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'item.html', context)
