from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth.models import Permission, User
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,"index.html",{})

# def login(request):
#     return render(request,"myUPS/login.html",{}) 

# def register(request):
#     return render(request,"myUPS/register.html",{})

# def package(request):
#     return render(request,"myUPS/package.html",{})

# def all_info(request):
#     return render(request,"myUPS/all_info.html",{})

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        account = Account()
        account.user = user
        world = World.objects.get(curr = True)
        world_id = world.world_id
        account.world = world
        account.save()
        if user is not None:
            if user.is_active:
                return redirect('login_user')
    context = {
        "form": form,
    }
    return render(request, 'myUPS/register.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')

            else:
                return render(request, 'myUPS/login.html', {'error_message': 'Invalid login'})
    return render(request, 'myUPS/login.html')

def track_pkg(request):
    pack_id = request.POST.get('package_number')
    context = {
        'pkgs':Package.objects.filter(pk = pack_id)
    }
    return render(request,'myUPS/package.html',context)

def all_pkg(request):
    user = request.user
    account = Account.objects.get(user_id = user.id)
    context = {
        'pkgs':Package.objects.filter(user_id = account.id)
    }
    return render(request,'myUPS/package.html',context)

def logout_user(request):
    logout(request)
    # form = ProfileForm(request.POST or None)
    # context = {
    #     "form": form,
    # }

    return redirect('login_user')

def edit_dest(request):
    # pack_id = request.POST.get('pkg.package_id')
    pack_id = request.GET.get('package_id', '')
    if pack_id == '':
        # if not request.user.is_active or not request.user.is_authenticated or request.user.username != pack.user.user.username:
        messages.warning(request, 'Please select a package!')
        return redirect("index")
        # else:
        #     return redirect('all_pkg')
    # user = request.user
    pack = Package.objects.get(pk = pack_id)
    print(request)
    if not request.user.is_active or not request.user.is_authenticated or pack.user == None or request.user.username != pack.user.user.username:
        messages.warning(request, 'You Don\'t Have Access To This Package!')
        messages.warning(request, 'Please Log In as owner!')
        logout_user(request)
        return redirect('login_user')
    if pack.cur_status != "p":
        if not request.user.is_active or not request.user.is_authenticated or request.user.username != pack.user.user.username:
            messages.warning(request, 'You can not change its destination! The package is already on its way!')
            return redirect("index")
        else:
            return redirect("all_pkg")
    context = {
        'pkg':Package.objects.get(pk = pack_id)
    }
    # print(request.GET.get('pkg.package_id'))
    return render(request,'myUPS/edit_dest.html', context)

def save_dest(request):
    pack_id = request.POST.get('package_id', '')
    dest_x = request.POST.get('destination_x', '')
    dest_y = request.POST.get('destination_y', '')
    print(pack_id)
    print(dest_x)
    print(dest_y)
    pack = Package.objects.get(pk = pack_id)
    pack.dest_x = str(dest_x)
    pack.dest_y = str(dest_y)
    pack.save()
    return redirect("all_pkg")
#become a prime, change boolean field into true
def become_prime(request):
    user = request.user
    account = Account.objects.get(user_id = user.id)
    return render(request,'myUPS/package.html',account)


def edit_email(request):
    form = EmailForm(request.POST or None)
    if form.is_valid():
        email_new = form.cleaned_data['email']
        user = request.user
        user.email = email_new
        user.save()
        return redirect('index')
    context = {
        "form": form,
    }
    return render(request, 'myUPS/edit_email.html', context)

@login_required
def loading(request):
    user = request.user
    account = Account.objects.get(user_id = user.id)
    context = {
        'pkgs':Package.objects.filter(user_id = account.id).filter(cur_status = 'p')
    }
    return render(request,'myUPS/package.html',context)

def out(request):
    user = request.user
    account = Account.objects.get(user_id = user.id)
    context = {
        'pkgs':Package.objects.filter(user_id = account.id).filter(cur_status = 'o')
    }
    return render(request,'myUPS/package.html',context)

def arrive(request):
    user = request.user
    account = Account.objects.get(user_id = user.id)
    context = {
        'pkgs':Package.objects.filter(user_id = account.id).filter(cur_status = 'd')
    }
    return render(request,'myUPS/package.html',context)