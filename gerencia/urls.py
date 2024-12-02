from django.urls import path
from .views import inicio_gerencia, listagem_noticia, cadastrar_noticia, editar_noticia, editar_categoria, remover_categoria, cadastrar_categoria

app_name = 'gerencia'

urlpatterns = [
    path('', inicio_gerencia, name='inicio_gerencia'),
    path('noticias/', listagem_noticia, name='listagem_noticia'),
    path('noticias/cadastro', cadastrar_noticia, name='cadastro_noticia'),
    path('noticias/editar/<int:id>', editar_noticia, name='editar_noticia'),
    path('categoria/editar/<int:id>/', editar_categoria, name='editar_categoria'),
    path('categoria/remover/<int:id>/', remover_categoria, name='remover_categoria'),
    path('categoria/cadastro/', cadastrar_categoria, name='cadastro_categoria')
]