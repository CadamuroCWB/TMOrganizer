from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ContactForm

from .models import Contact

# CRUD: List contacts
@login_required
def contact_list(request):
    contacts = Contact.objects.all()
    context = {
        'contact_info': contacts,
        'title': 'Techno Mania - Contato',
        'msg_title': 'Cadastrar contatos',
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
    }
    return render(request, 'contact_confirm_delete.html', context)
