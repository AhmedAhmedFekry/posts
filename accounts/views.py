from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import SignForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import View
from accounts.models import UserProfile

# Create your views here.
############## class based view generic ###################


def show_profile(request):
    return render(request, 'accounts/profile.html', {})


def user_update(request):
    if request.method == 'POST':
        # request.user is user  data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profiles)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return HttpResponseRedirect('/profile/')
    else:

        user_form = UserUpdateForm(instance=request.user)
        # "userprofile" model -> OneToOneField relatinon with user
        profile_form = ProfileUpdateForm(instance=request.user.profiles)
        context = {

            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'accounts/update.html', context)


class SignUpView(View):
    def post(self, request):
        form = SignForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:

                login(request, user)
                profile = UserProfile.objects.create(user=user).save()
                print('create profile is done ')
                return redirect('home')

    def get(self, request):
        form = SignForm()
        return render(request, 'accounts/sginup.html', {'form': form})


# def sign_up(request):
#     if request.POST:
#         username = request.POST.get('name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password1 = request.POST.get('password1')
#         if password == password1:
#             user = User.objects.create_user(
#                 username=username, email=email, password=password1).save()
#             return redirect('boards')

#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('boards')
#         else:
#             return redirect('login')
#         print(username, password)
#     else:
#         return render(request, 'accounts/sginup.html', {})

##################### the second method for sign up functions ased view #############################

# def sign_up(request):
#     if request.user.is_authenticated:
#         return redirect('boards')
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid:
#             form.save()
#             return redirect('boards')
#     else:
#         form = UserCreationForm()

#     return render(request, 'accounts/sginup.html', {'form': form})

### third method for sign up  functions ased view####################

# def sign_up(request):
#     if request.user.is_authenticated:
#         return redirect('boards')
#     if request.method == 'POST':
#         form = SignForm(request.POST)
#         if form.is_valid():
#             # form.save(commit=False)
#             form.save()
#             username = request.POST.get('username')
#             password = request.POST.get('password1')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('boards')
#     else:
#         form = SignForm()
#         return render(request, 'accounts/sginup.html', {'form': form})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('boards')
    if request.POST:
        form = SignForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
        username = request.POST.get('username')
        password = request.POST.get('password1')
        form.save()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('boards')
        else:
            return redirect('login')
        print(username, password)
    else:
        form = SignForm()
        return render(request, 'accounts/login.html', {'form': form})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.POST:

        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
        print(username, password)
    else:
        return render(request, 'accounts/login.html', {})


def log_out(request):
    logout(request)
    return redirect('boards')
