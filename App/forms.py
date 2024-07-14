from django import forms
from django.contrib.auth.models import User
from .models import Profile, Resource, Alert, ResourceRequest, ForumPost, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
# from .models import CustomUser



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone_number = forms.CharField(max_length=20, label='Phone_number')
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # password = forms.CharField(widget=forms.PasswordInput)
    # confirm_password = forms.CharField(widget=forms.PasswordInput)
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ['username', 'email',  'phone_number',  'first_name', 'last_name' ,'location',]


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("passwords do not match")
        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )



class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description', 'available']


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['title', 'description', 'location', 'is_active', 'visibility']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'email', 'phone_number']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }



class SuperuserProfileForm(ProfileForm):
    pass


class ResourceRequestForm(forms.ModelForm):
    class Meta:
        model = ResourceRequest
        fields = ['Resource_type', 'description']


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']

   
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class FormComment(forms.ModelForm):
    class  Meta:
        model = Comment
        fields = ('name',  'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),

        }

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'phone_number', 'location')


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Passowrd'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Conform new password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

