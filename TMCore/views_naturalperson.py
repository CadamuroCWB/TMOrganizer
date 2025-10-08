from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import NaturalPerson
from .forms_naturalperson import NaturalPersonForm

@login_required
def naturalperson_list(request):
    people = NaturalPerson.objects.select_related('owner_company', 'user').all()
    context = {
        'people': people,
        'title': 'Techno Mania - Pessoas Físicas',
        'msg_title': 'Pessoas Físicas',
        'description': 'Cadastro de pessoas físicas aqui.',
        'keywords': 'pessoas físicas, cadastro, gerenciamento',
        'date': date.today(),
    }
    return render(request, 'naturalperson_list.html', context)

@login_required
def naturalperson_create(request):
    if request.method == 'POST':
        form = NaturalPersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pessoa física criada com sucesso!')
            return redirect('naturalperson_list')
    else:
        form = NaturalPersonForm()
    context = {
        'form': form,
        'title': 'Techno Mania - Pessoas Físicas',
        'msg_title': 'Pessoas Físicas',
        'description': 'Cadastro de pessoas físicas aqui.',
        'keywords': 'pessoas físicas, cadastro, gerenciamento',
        'date': date.today(),
    }
    return render(request, 'naturalperson_form.html', context)

@login_required
def naturalperson_update(request, pk):
    person = get_object_or_404(NaturalPerson, pk=pk)
    if request.method == 'POST':
        form = NaturalPersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pessoa física atualizada com sucesso!')
            return redirect('naturalperson_list')
    else:
        form = NaturalPersonForm(instance=person)
    context = {
        'form': form,
        'title': 'Techno Mania - Pessoas Físicas',
        'msg_title': 'Pessoas Físicas',
        'description': 'Cadastro de pessoas físicas aqui.',
        'keywords': 'pessoas físicas, cadastro, gerenciamento',
        'date': date.today(),
    }
    return render(request, 'naturalperson_form.html', context)

@login_required
def naturalperson_delete(request, pk):
    person = get_object_or_404(NaturalPerson, pk=pk)
    if request.method == 'POST':
        person.delete()
        messages.success(request, 'Pessoa física excluída com sucesso!')
        return redirect('naturalperson_list')
    context = {
        'object': person,
        'title': 'Techno Mania - Pessoas Físicas',
        'msg_title': 'Pessoas Físicas',
        'description': 'Cadastro de pessoas físicas aqui.',
        'keywords': 'pessoas físicas, cadastro, gerenciamento',
        'date': date.today(),
    }
    return render(request, 'naturalperson_confirm_delete.html', context)
