from django import forms
from .models import Player
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class PlayerEditForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('img','age','starsign')

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            raise forms.ValidationError("This username has already been registered")
        return super(UserRegisterForm, self).clean(*args, **kwargs)

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Username does not exist or incorrect password')
            # if not user.check_password(password):
            #     raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)