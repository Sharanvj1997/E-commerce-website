from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Import User from Django's built-in auth system

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User  # Corrected typo from 'moddel' to 'model'
        fields = ['username', 'email', 'password1', 'password2']
