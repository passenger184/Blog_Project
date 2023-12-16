from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from users.forms import UserRegisterForm, UserUpdateForm, UserProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def register(request):
    
    if request.method == 'POST':
         form = UserRegisterForm(request.POST)
         if form.is_valid():
             form.save()
             username = form.cleaned_data.get('username')
             messages.success(request, f'Account created successfully for {username}')
             return redirect('login')
    else:
         form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, 'users.html', context)


'''
messages.debug
messages.info
messages.success
messages.warning
messages.error

'''

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, 'Your account has been Updated!')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)   
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    
    return render(request, 'profile.html', context)