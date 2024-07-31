# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(label='自己紹介:',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Tell us about yourself...'}),
        required=False)
    profile_picture = forms.ImageField(label='画像:', required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'bio', 'profile_picture', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.bio = self.cleaned_data['bio']
        if self.cleaned_data['profile_picture']:
            user.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            user.save()
        return user
