from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Django REST Framework imports
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .forms import ContactForm
from .models import Contact, Client
from .serializers import ClientSerializer, ClientListSerializer, ContactSerializer

# CRUD: List contacts
@login_required
def contact_list(request):
    contacts = Contact.objects.all()
    context = {
        'contact_info': contacts,
        'title': 'Techno Mania - Contato',
        'msg_title': 'Cadastrar contatos',
        'date': date.today(),
    }
    return render(request, 'contact_list.html', context)

# CRUDE: Create contact
@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato criado com sucesso!')
            return redirect('contact_list')
    else:
        form = ContactForm()
    context = {
        'form': form,
        'title': 'Techno Mania - Novo Contato',
        'msg_title': 'Criar novo contato',
        'date': date.today(),
    }
    return render(request, 'contact_form.html', context)

# CRUDE: Update contact
@login_required
def contact_update(request, pk):
    obj = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato atualizado com sucesso!')
            return redirect('contact_list')
    else:
        form = ContactForm(instance=obj)
    context = {
        'form': form,
        'title': 'Techno Mania - Editar Contato',
        'msg_title': 'Editar contato',
        'date': date.today(),
    }
    return render(request, 'contact_form.html', context)

# CRUDE: Delete contact
@login_required
def contact_delete(request, pk):
    obj = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Contato excluído com sucesso!')
        return redirect('contact_list')
    context = {
        'object': obj,
        'title': 'Techno Mania - Excluir Contato',
        'msg_title': 'Tem certeza de que deseja excluir este contato?',
        'date': date.today(),
    }
    return render(request, 'contact_confirm_delete.html', context)


# ============================================================================
# CLASS-BASED VIEWS (CBVs) - Alternativa elegante ao CRUD tradicional
# ============================================================================

class ClientListView(LoginRequiredMixin, ListView):
    """Lista de clientes com paginação e busca"""
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Client.objects.all()
        search = self.request.GET.get('search')
        regime = self.request.GET.get('regime')
        end_consumer = self.request.GET.get('end_consumer')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(cnpj__icontains=search) |
                Q(alias__icontains=search) |
                Q(email__icontains=search)
            )
        
        if regime:
            queryset = queryset.filter(tax_regime=regime)
            
        if end_consumer:
            queryset = queryset.filter(end_consumer=end_consumer == 'true')
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()
        context['title'] = 'Techno Mania - Clientes'
        context['search'] = self.request.GET.get('search', '')
        context['regime'] = self.request.GET.get('regime', '')
        context['end_consumer'] = self.request.GET.get('end_consumer', '')
        context['tax_regimes'] = Client.TAX_REGIME_CHOICES
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Detalhes do cliente"""
    model = Client
    template_name = 'client_detail.html'
    context_object_name = 'client'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()
        context['title'] = f'Cliente - {self.object.name}'
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Criação de cliente"""
    model = Client
    template_name = 'client_form.html'
    fields = [
        'name', 'alias', 'cnpj', 'email', 'phone', 'address',
        'start_date', 'tax_regime', 'legal_nature', 'end_consumer',
        'subject_protest', 'logo', 'isic', 'home_directory'
    ]
    success_url = reverse_lazy('client_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()
        context['title'] = 'Novo Cliente'
        context['action'] = 'Criar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente criado com sucesso!')
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Edição de cliente"""
    model = Client
    template_name = 'client_form.html'
    fields = [
        'name', 'alias', 'cnpj', 'email', 'phone', 'address',
        'start_date', 'tax_regime', 'legal_nature', 'end_consumer',
        'subject_protest', 'logo', 'isic', 'home_directory'
    ]
    success_url = reverse_lazy('client_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar Cliente - {self.object.name}'
        context['action'] = 'Atualizar'
        context['date'] = date.today()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Exclusão de cliente"""
    model = Client
    template_name = 'client_confirm_delete.html'
    context_object_name = 'client'
    success_url = reverse_lazy('client_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Excluir Cliente - {self.object.name}'
        context['date'] = date.today()
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cliente excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# DJANGO REST FRAMEWORK VIEWSETS - Alternativa moderna ao CRUD tradicional
# ============================================================================

class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para Client com funcionalidades avançadas:
    - CRUD automático via API REST
    - Filtros e busca
    - Ações personalizadas
    - Paginação automática
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    
    # Configuração de filtros e busca
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tax_regime', 'legal_nature', 'end_consumer', 'subject_protest']
    search_fields = ['name', 'cnpj', 'alias', 'email', 'phone']
    ordering_fields = ['name', 'start_date', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Usa serializer simplificado para listagem"""
        if self.action == 'list':
            return ClientListSerializer
        return ClientSerializer
    
    @action(detail=False, methods=['get'])
    def end_consumers(self, request):
        """Endpoint para listar apenas consumidores finais"""
        clients = self.queryset.filter(end_consumer=True)
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_tax_regime(self, request):
        """Endpoint para filtrar por regime tributário"""
        regime = request.query_params.get('regime')
        if regime:
            clients = self.queryset.filter(tax_regime=regime)
            serializer = self.get_serializer(clients, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro regime é obrigatório'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def toggle_end_consumer(self, request, pk=None):
        """Alterna status de consumidor final"""
        client = self.get_object()
        client.end_consumer = not client.end_consumer
        client.save()
        return Response({
            'status': 'success',
            'end_consumer': client.end_consumer,
            'message': f'Cliente {"marcado" if client.end_consumer else "desmarcado"} como consumidor final'
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Endpoint com estatísticas dos clientes"""
        total = self.queryset.count()
        end_consumers = self.queryset.filter(end_consumer=True).count()
        by_regime = {}
        
        for regime_code, regime_name in Client.TAX_REGIME_CHOICES:
            count = self.queryset.filter(tax_regime=regime_code).count()
            by_regime[regime_name] = count
        
        return Response({
            'total_clients': total,
            'end_consumers': end_consumers,
            'non_end_consumers': total - end_consumers,
            'by_tax_regime': by_regime
        })


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet para Contact com funcionalidades básicas"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'cpf', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
