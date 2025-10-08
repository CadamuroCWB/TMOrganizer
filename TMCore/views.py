from datetime import date
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# main views
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from datetime import datetime, timedelta

from .forms import ContactUsForm, CompanyForm
from .models import Company, Person, Calendar, Event
from .serializers import PersonSerializer, EventSerializer

# API ViewSets
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
@api_view(['GET'])
def get_events_by_week(request):
    """
    Retorna eventos para uma semana específica.
    Parâmetro: week_start (formato: YYYY-MM-DD) - Data de início da semana
    """
    try:
        week_start_str = request.GET.get('week_start')
        if not week_start_str:
            # Se não for fornecida uma data, usa a data atual
            week_start = datetime.now().date()
            week_start = week_start - timedelta(days=week_start.weekday())  # Ajusta para segunda-feira
        else:
            week_start = datetime.strptime(week_start_str, '%Y-%m-%d').date()
            
        # Ajusta para domingo (início da semana)
        week_start = week_start - timedelta(days=week_start.weekday() + 1)
        week_end = week_start + timedelta(days=7)
        
        # Busca eventos que ocorrem durante a semana
        events = Event.objects.filter(
            start_datetime__date__gte=week_start,
            start_datetime__date__lt=week_end
        ).order_by('start_datetime')
        
        # Serializa os eventos
        serializer = EventSerializer(events, many=True)
        
        # Organiza os eventos por dia da semana
        events_by_day = {
            'sunday': [],
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': []
        }
        
        day_mapping = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday'
        }
        
        for event in serializer.data:
            event_date = datetime.strptime(event['start_datetime'], '%Y-%m-%dT%H:%M:%SZ').date()
            day_of_week = event_date.weekday()
            day_name = day_mapping[day_of_week]
            events_by_day[day_name].append(event)
        
        return Response({
            'week_start': week_start.strftime('%Y-%m-%d'),
            'week_end': week_end.strftime('%Y-%m-%d'),
            'events_by_day': events_by_day
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# Dolar

# CRUD: List companies
@login_required
def company_list(request):
    companies = Company.objects.all()
    events = Event.objects.filter(company__in=companies)
    context = {
        'companies': companies,
        'title': 'Lista de empresas',
        'msg_title': 'Cadastrar empresas',
        'date': date.today(),
    }
    return render(request, 'company_list.html', context)


# CRUD: Create company
@login_required
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa criada com sucesso!')
            return redirect('company_list')
    else:
        form = CompanyForm()
    context = {
        'form': form, 
        'title': 'Techno Mania - Adicionar',
        'msg_title': 'Adicionar nova empresa',
        'date': date.today(),
    }
    return render(request, 'company_form.html', context)


# CRUD: Update company
@login_required
def company_update(request, pk):
    obj = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa atualizada com sucesso!')
            return redirect('company_list')
    else:
        form = CompanyForm(instance=obj)
    context = {
        'form': form, 
        'title': 'Techno Mania - Editar',
        'msg_title': 'Alterar {{ obj.name }}',
        'date': date.today(),
    }
    return render(request, 'company_form.html', context)


# CRUD: Delete company
@login_required
def company_delete(request, pk):
    obj = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Empresa excluída com sucesso!')
        return redirect('company_list')
    context = {
        'object': obj, 
        'title': 'Techno Mania - Excluir',
        'msg_title': 'Tem certeza de que deseja excluir esta empresa?',
        'date': date.today(),
    }
    return render(request, 'company_confirm_delete.html', context)

@login_required
def calendar(request, week_number=0, year=None):
    if not year: 
        year = date.today().year
    if not week_number:
        week_number = date.today().isocalendar()[1]
    
    # Buscar empresas do usuário logado ou todas as empresas se for superuser
    if request.user.is_superuser:
        companies = Company.objects.all()
    else:
        companies = Company.objects.filter(owner=request.user)
    
    events = Event.objects.filter(company__in=companies)
    context = {
        'companies': companies,
        'events': events,
        'title': 'Techno Mania - Calendário',
        'msg_title': 'Agendamentos',
        'description': 'Faça seus agendamentos aqui.',
        'keywords': 'calendário, eventos, datas importantes',
        'current_month': date.today().month,
        'week_number': week_number,
        'year': year,
        'date': date.today(),
    }
    return render(request, 'calendar.html', context)

@csrf_exempt
def event_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Event.objects.create(
            title=data['title'],
            date=data['date'],
            # ... outros campos
        )
        return JsonResponse({'success': True})

@login_required
def opening_hours(request):
    context = {
        'title': 'Techno Mania - Horário de Funcionamento',
        'msg_title': 'Horários de Funcionamento',
        'description': 'Gerencie os horários de funcionamento da sua empresa.',
        'keywords': 'horário de funcionamento, empresa, agendamento',
        'date': date.today(),
    }
    return render(request, 'opening_hours.html', context)

# public views
def about(request):
    context = {
        'title': 'Techno Mania - Sobre',
        'msg_title': 'Soluções para o entusiasta da tecnologia. Soluções inteligentes para um mundo antenado em tecnologia.',
        'description': 'Bem-vindo à Techno Mania, sua fonte de referência para o que há de mais recente em tecnologia, oferecendo insights e soluções para entusiastas da tecnologia. Explore o que há de mais recente em tecnologia com a Techno Mania.',
        'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
        'date': date.today(),}
    return render(request, 'about.html', context)

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
    form = ContactUsForm()
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
        'date': date.today(),
    }
    return render(request, 'contactus.html', context)

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': '',
            'msg_title': 'Escolha a linha de produtos que mais combina com você',
            'description': '',
            'keywords': 'technology, gadgets, software, reviews, ERP, CRM, AI, IoT, BI',
            'date': date.today(),
        })
        return context  

# error handlers
def custom_404_view(request, exception):
    context = {
        'title': 'Page Not Found',
        'msg_title': 'The page you are looking for does not exist.',
        'description': '',
        'keywords': '',
        'date': date.today(),
    }
    return render(request, '404', context, status=404)

def custom_500_view(request):
    context = {
        'title': 'Server Error',
        'msg_title': 'An unexpected error occurred.',
        'description': '',
        'keywords': '',
        'date': date.today(),
    }
    return render(request, '500.html', context, status=500)
