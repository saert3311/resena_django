from django import forms
from django.forms import ModelForm
from .models import *

class RegisterForm(forms.Form):
    f_name = forms.CharField(max_length=50)
    l_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_password(self):
        password = self.cleaned_data['password']
        print(self.cleaned_data)
        password_repeat = self.cleaned_data['password_repeat']
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if password != password_repeat:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username','first_name', 'last_name', 'user_type']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class ReviewForm(ModelForm):
    STAR_CHOICES = (
    (1, '🫥'),
    (2, '🫥😑'),
    (3, '🫥😑😊'),
    (4, '🫥😑😊😍'),
    (5, '🫥😑😊😍🤩'),
)
    rating = forms.ChoiceField(choices=STAR_CHOICES, label='Rating')
    class Meta:
        model = Review
        fields = '__all__'

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'