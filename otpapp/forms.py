from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import User
from django_otp.oath import TOTP

class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    # is_verified = forms.BooleanField(initial=False)
    
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        # user.is_verified = False
        totp = TOTP("JBSWY3DPEHPK3PXP")
        token_number = totp.token()
        user.token_number = token_number
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            
        return user
    
class VerificationForm(forms.Form):
    token_numer = forms.CharField(max_length=6, required=True)
    
    class Meta:
        fields = ('token_numer')
        
    def getToken(self):
        self.full_clean()
        return self.cleaned_data['token_numer']