from django.shortcuts import render, redirect
from .forms import NoticiaForm, NoticiaFilterForm, CategoriaForm
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .models import Noticia, Categoria

def login_required_message(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Você precisa estar logado para acessar a página solicitada.')
            return redirect(reverse_lazy('usuarios:login'))
        return view_func(request, *args, **kwargs)
    return wrapper

# Create your views here.
@login_required_message
def inicio_gerencia(request):
    search_query = request.GET.get('search')

    if not search_query:
        categorias = Categoria.objects.all()
    else:
        categorias = Categoria.objects.filter(Q(nome__icontains=search_query))

    categorias = categorias.order_by('nome')
    
    paginator = Paginator(categorias, 5)
    page = request.GET.get('page', 1)
    categorias_paginadas = paginator.page(page)

    contexto = {
        'categorias': categorias_paginadas,
        'search_query': search_query,
        'page_obj': categorias_paginadas,
    }
    
    return render(request, 'categoria/index.html', contexto)

@login_required_message
def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            if Categoria.objects.filter(nome=nome).exclude(id=id).exists():
                form.add_error('nome', 'A categoria com este nome já existe.')
            else:
                form.save()
                return redirect('gerencia:inicio_gerencia')
    else:
        form = CategoriaForm(instance=categoria)
    
    contexto = {
        'form': form
    }
    return render(request, 'gerencia/cadastro_categoria.html', contexto)

@login_required_message
def remover_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('gerencia:inicio_gerencia')
    
    contexto = {
        'categoria': categoria
    }
    return render(request, 'gerencia/remover_categoria.html', contexto)

@login_required_message
def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            if Categoria.objects.filter(nome=nome).exists():
                form.add_error('nome', 'A categoria com este nome já existe.')
            else:
                form.save()
                return redirect('gerencia:inicio_gerencia')
    else:
        form = CategoriaForm()
    
    contexto = {
        'form': form
    }
    return render(request, 'gerencia/cadastro_categoria.html', contexto)

@login_required_message
def listagem_noticia(request):
    formularioFiltro = NoticiaFilterForm(request.GET or None)
    
    noticias = Noticia.objects.filter(usuario=request.user)  # Filtra pelo usuário logado

    if formularioFiltro.is_valid():
        if formularioFiltro.cleaned_data['titulo']:
            noticias = noticias.filter(titulo__icontains=formularioFiltro.cleaned_data['titulo'])
        if formularioFiltro.cleaned_data['data_publicacao_inicio']:
            noticias = noticias.filter(data_publicacao__gte=formularioFiltro.cleaned_data['data_publicacao_inicio'])
        if formularioFiltro.cleaned_data['data_publicacao_fim']:
            noticias = noticias.filter(data_publicacao__lte=formularioFiltro.cleaned_data['data_publicacao_fim'])
        if formularioFiltro.cleaned_data['categoria']:
            noticias = noticias.filter(categoria=formularioFiltro.cleaned_data['categoria'])
    
    contexto = {
        'noticias': noticias,
        'formularioFiltro': formularioFiltro
    }
    return render(request, 'gerencia/listagem_noticia.html',contexto)

@login_required_message
def cadastrar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)  # Cria instância sem salvar
            noticia.usuario = request.user  # Atribui o autor (usuário logado)
            noticia.save()  # Salva a notícia no banco
            return redirect('gerencia:listagem_noticia')  # Redireciona para página de sucesso
    else:
        form = NoticiaForm() 

    contexto = {'form': form}
    return render(request, 'gerencia/cadastro_noticia.html', contexto)

@login_required_message
def editar_noticia(request, id):
    noticia = Noticia.objects.get(id=id)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia_editada = form.save(commit=False)  # Não salva ainda
            noticia_editada.usuario = request.user 
            noticia_editada.save()  # Salva com o usuário intacto
            return redirect('gerencia:listagem_noticia')
    else:
        form = NoticiaForm(instance=noticia)
    
    contexto = {
        'form': form
    }
    return render(request, 'gerencia/cadastro_noticia.html',contexto)

def index(request):
    categoria_nome = request.GET.get('categoria')  # Obtém o parâmetro 'categoria' da URL
    search_query = request.GET.get('search')  # Obtém o parâmetro de busca

    # Filtra as notícias com base na categoria ou na busca
    noticias = Noticia.objects.all()
    if categoria_nome:
        categoria = Categoria.objects.filter(nome=categoria_nome).first()
        if categoria:
            noticias = noticias.filter(categoria=categoria)

    if search_query:
        noticias = noticias.filter(titulo__icontains=search_query)  # Filtra por título, ignorando maiúsculas/minúsculas

    categorias = Categoria.objects.all()  # Pega todas as categorias para exibir no template

    contexto = {
        'noticias': noticias,
        'categorias': categorias,
        'categoria_selecionada': categoria_nome,
        'search_query': search_query,
    }
    return render(request, 'gerencia/index.html', contexto)
