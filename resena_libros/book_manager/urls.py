from django.urls import path
from .views import *

app_name = 'book_manager'

urlpatterns = [
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('registro/', register_view, name='register'),
    path('salir/', logout_view, name='logout'),
    path('perfil/', edit_profile_view, name='edit_profile'),
    path('generos/', list_genre, name='list_genre'),
    path('generos/<int:pk>/editar/', GenreUpdateView.as_view(), name='update_genre'),
    path('generos/<int:pk>/eliminar/', GenreDeleteView.as_view(), name='delete_genre'),
    path('autores/', list_authors, name='list_author'),
    path('autores/<int:pk>/editar/', AuthorUpdateView.as_view(), name='update_author'),
    path('autores/<int:pk>/eliminar/', AuthorDeleteView.as_view(), name='delete_author'),
    path('libros/nuevo/', BookCreateView.as_view(), name='create_book'),
    path('libros/<int:pk>/', detail_book, name='detail_book'),
    path('libros/<int:pk>/editar/', BookUpdateView.as_view(), name='update_book'),
    path('libros/<int:pk>/eliminar/', BookDeleteView.as_view(), name='delete_book'),
    path('reviews/create/', create_review, name='create_review'),
    path('contacts/', list_contacts, name='list_contacts'),
]