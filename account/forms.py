from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser



class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class UserRegistrationForm(UserCreationForm):
    ACCOUNT_TYPE = (("admin", "Admin"), ("voter", "Voter"))
    birth_date = forms.DateField(null=True, blank=True)
    user_type = forms.CharField(default="voter", choices=ACCOUNT_TYPE, max_length=6)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth_date','user_type']
        
        # form.save()
    def save(self, commit=True):
        our_user = super().save(commit=False) # ami database e data save korbo na ekhn
        if commit == True:
            our_user.save() # user model e data save korlam
            birth_date = self.cleaned_data.get('birth_date')
            user_type = self.cleaned_data.get('user_type')
            CustomUser.objects.create(
                user = our_user,
                user_type=user_type,
                birth_date =birth_date,
            )
        return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })

