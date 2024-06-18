from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Genre, Author, Book, Review, Contact
from .forms import RegisterForm, UserUpdateForm, GenreForm, AuthorForm, ReviewForm, ContactForm
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.db.models import Q

# Create your views here.
def index_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Mensaje enviado exitosamente.')
        else:
            for field, errors in contact_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    search_term = request.GET.get('search')
    if search_term:
        q = Q(title__icontains=search_term) | Q(description__icontains=search_term) | Q(publication_year__icontains=search_term) | Q(author__name__icontains=search_term) | Q(genre__name__icontains=search_term)
        books = Book.objects.filter(q).order_by('title')
    else:
        books = Book.objects.all().order_by('title')
    contact_form = ContactForm()
    return render(request, 'index.html', {'pagetitle': 'Home', 'books': books, 'contact_form': contact_form, 'search_term': search_term})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('book_manager:index')
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username_or_email, email=username_or_email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.first_name}!')
            return redirect('book_manager:index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'pagetitle': 'Iniciar sesión'})     

def register_view(request):
    if request.user.is_authenticated:
        return redirect('book_manager:index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data
                user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'], first_name=data['f_name'], last_name=data['l_name'])
                messages.success(request, 'Usuario creado exitosamente.')
                return redirect('book_manager:login')
        except ValidationError as e:
            for message in e.messages:
                messages.error(request, message)
            return redirect('book_manager:register')
    form = RegisterForm()
    return render(request, 'register.html', {'form':form, 'pagetitle':'Registro'})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('book_manager:index')


@login_required
def edit_profile_view(request):
    password_form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if 'update_profile' in request.POST and user_form.is_valid():
            user_form.save()
            request.user = User.objects.get(id=request.user.id)
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('book_manager:index')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user) 
                messages.success(request, 'Contraseña actualizada exitosamente.')
                return redirect('book_manager:index')
            else:
                #add form errors to messages
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    user_form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {
        'pagetitle':'Perfil', 
        'user_form': user_form, 
        'password_form': password_form, 
    })
#GENRES
@login_required
def list_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Género creado exitosamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    genres = Genre.objects.all().order_by('name')
    form = GenreForm()
    num_genres = genres.count()
    return render(request, 'genre/list.html', {'genres': genres, 'pagetitle': 'Géneros', 'num_genres': num_genres, 'form': form})

class GenreDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Genre
    success_url = '/generos/'
    template_name = 'layouts/confirm_delete.html'
    context_object_name = 'genre'
    success_message = 'Género eliminado exitosamente.'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagetitle'] = 'Eliminar género'
        return context

class GenreUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Genre
    fields = ['name']
    template_name = 'genre/update.html'
    success_url = '/generos/'
    success_message = 'Género actualizado exitosamente.'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagetitle'] = 'Actualizar género'
        return context
#AUTHORS
@login_required
def list_authors(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor creado exitosamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    authors = Author.objects.all().order_by('name')
    form = AuthorForm()
    author_count = authors.count()
    return render(request, 'author/list.html', {'authors': authors, 'pagetitle': 'Autores', 'author_count': author_count, 'form': form})

class AuthorDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Author
    success_url = '/autores/'
    template_name = 'layouts/confirm_delete.html'
    context_object_name = 'author'
    success_message = 'Autor eliminado exitosamente.'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagetitle'] = 'Eliminar Autor'
        return context

class AuthorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Author
    fields = ['name']
    template_name = 'author/update.html'
    success_url = '/autores/'
    success_message = 'Autor actualizado exitosamente.'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagetitle'] = 'Actualizar autor'
        return context

#BOOKS

class BookCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Book
    fields = ['title', 'description', 'publication_year', 'cover', 'author', 'genre']
    template_name = 'book/create.html'
    success_url = '/'
    success_message = 'Libro creado exitosamente.'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagetitle'] = 'Crear libro'
        return context

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return response

class BookUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    fields = ['title', 'description', 'publication_year', 'cover', 'author', 'genre']
    template_name = 'book/update.html'
    success_url = '/'
    success_message = 'Libro actualizado exitosamente.'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagetitle'] = 'Actualizar libro'
        return context

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return response
    
class BookDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Book
    success_url = '/'
    template_name = 'layouts/confirm_delete.html'
    context_object_name = 'book'
    success_message = 'Libro eliminado exitosamente.'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagetitle'] = 'Eliminar libro'
        return context

def detail_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        #add user and book to form
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.book = book
            obj.save()
            messages.success(request, 'Reseña creada exitosamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    reviews = Review.objects.filter(book=book)
    review_form = ReviewForm(initial={'book': book, 'user': request.user})
    return render(request, 'book/show.html', {'book': book, 'pagetitle': book.title, 'reviews': reviews, 'review_form': review_form})

#REVIEWS

def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reseña creada exitosamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        return redirect('book_manager:index')
    return redirect('book_manager:index')


#CONTACT
@login_required
def list_contacts(request):
    contacts = Contact.objects.all()
    return render(request, 'contacts.html', {'contacts': contacts, 'pagetitle': 'Contactos'})