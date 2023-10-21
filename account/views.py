from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm, Changepass, Change_pass
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm


# new coder code for toster
def account_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)        
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('userDashboard')
        else:
            messages.error(request, "Invalid details")
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html')



# Normal user register function
def account_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. You can login now!")
            return redirect('userDashboard')
        else:
            messages.error(request, "Provided data failed validation")
            # return account_login(request)
    else :
        form = RegistrationForm()        
    return render(request, 'account/register.html', {'form': form})




# def user_registration(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('myprofile') 
#     else:
#         form = RegistrationForm()
#     return render(request, 'account/register.html', {'form': form})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('myprofile')
#         else:
#             pass
#     return render(request, 'account/login.html')



def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect('login') 


# user register with email varification
# def user_registration(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active=False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = "Activate Your Account"
#             message = render_to_string('account/varify_email.html',{
#                 'user': request.user,
#                 'domain':current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
                
#             })
#             send_mail = form.cleaned_data.get('email')
#             email = EmailMessage(mail_subject, message, to=[send_mail])
#             email.send()
#             messages.success(request, 'Account Created Successfully')
#             messages.info(request, 'Activate your account from your provided email')
#             # login(request, user)
#             return redirect('login') 
#     else:
#         form = RegistrationForm()
#     return render(request, 'account/register.html', {'form': form})


# Account acivation function from email here
# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Congratulations! Your account is activated. You Can login now')
#         return redirect('login')
#     else:
#         messages.error(request, 'Invalid activation link')
#         return redirect('register')



# change password with old password
# def pass_change(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':        
#             form = Changepass(user=request.user, data=request.POST) # user data collect kora hocce
#             if form.is_valid():
#                 form.save()
#                 update_session_auth_hash(request, form.user) # password update kora hocce
#                 messages.success('Your password updated successfully')
#                 return redirect('myprofile')
#         else:
#             form = Changepass(user = request.user)
#         return render(request, 'account/pass_change.html', {'form':form})
#     return redirect('login')




# change passsword without old password
def change_pass(request):
    # if request.user.is_authenticated:
    form = Change_pass(user=request.user, data=request.POST) # user data collect kora hocce
    if request.method == 'POST':        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # password update kora hocce
            # messages.success('Your Password updated successfully')
            return redirect('myprofile')
        
        else:
            form = Change_pass(user = request.user)
    return render(request, 'account/pass_change.html', {'form':form})
    # return redirect('change_pass')






# def forgotPassword(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         if request.user.exists():
#             user = request.user.get(email__exact=email)
#             # Reset password email
#             current_site = get_current_site(request)
#             mail_subject = 'Reset Your Password'
#             message = render_to_string('accounts/reset_password_email.html', {
#                 'user': user,
#                 'domain': current_site,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
#             })
#             to_email = email
#             send_email = EmailMessage(mail_subject, message, to=[to_email])
#             send_email.send()

#             messages.success(request, 'Password reset email has been sent to your email address.')
#             return redirect('login')
#         else:
#             messages.error(request, 'Account does not exist!')
#             return redirect('forgot_password')
#     return render(request, 'account/forgot_password.html')





def team_profile(request):
    return render(request,'account/footer/team.html')

def about(request):
    return render(request, 'account/footer/about.html')