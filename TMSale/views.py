from django.shortcuts import render
from django.http import HttpRequest

# main views
def item(request):
    context = {
        'title': 'Techno Mania - Item',
        'message': 'Os melhores produtos para você',
        'description': 'Explore nossa gama de produtos projetados para melhorar sua experiência tecnológica.',
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
    }
    return render(request, 'item.html', context)

