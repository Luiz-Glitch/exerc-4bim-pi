from django.urls import path

from . import views

app_name = 'gerencia'

urlpatterns = [
    path('', views.inicio_gerencia, name='gerencia_inicial'),
    path('noticias/', views.listagem_noticia, name='listagem_noticia'),
    path('noticias/cadastro', views.cadastrar_noticia, name='cadastro_noticia'),
    path('noticias/editar/<int:id>', views.editar_noticia, name='editar_noticia'),
    path('categorias/', views.listagem_categoria, name='listagem_categoria'),
    path('categorias/editar/<int:id>', views.editar_categoria, name='editar_categoria'),
    path('categorias/cadastro/', views.cadastro_categoria, name='cadastro_categoria'),
    path('categorias/excluir/<int:id>', views.excluir_categoria, name='excluir_categoria'),
    # Add your URL patterns here
]