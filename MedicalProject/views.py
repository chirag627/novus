from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from set.models import Set, Module, AttemptedSet

def index(request):
    if request.user.is_authenticated:
        return redirect('/modules')
    return redirect('/login')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/modules')
    else:
        if request.method == "POST":
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            return render(request, 'login.html', {'err': 'Invalid credentials!'})
        return render(request, 'login.html')

def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            print('hey')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(username=username, first_name=first_name, last_name=last_name, password=password)
                user.save()
                print(user)
            if user is not None:
                login(request, user)
                return redirect('/')
        return render(request, 'signup.html')
    return redirect('/')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


# for admin

def admin_panel(request):
    if request.user.is_superuser:
        attempted_sets = AttemptedSet.objects.all()
        modules = Module.objects.all()
        students = User.objects.filter(is_staff=False)
        return render(request, 'admin.html', {'admin': request.user, 'attempted_sets':attempted_sets, 'modules':modules, 'students':students})
    else:
        return redirect('/admin-panel/login/')


def admin_login(request):
    if request.user.is_superuser:
        return redirect('/admin-panel/')
    else:
        if request.method == "POST":
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if username and password:
                admin = authenticate(username=username, password=password)
                if admin is not None:
                    login(request, admin)
                    return redirect('/admin-panel/')
        return render(request, 'admin-login.html', )


def admin_logout(request):
    if request.user.is_superuser:
        logout(request)
    return redirect('/admin-panel/login/')


def list_students(request):
    if request.user.is_superuser:
        students = User.objects.filter(is_superuser=False, is_staff=False)
        return render(request, 'admin-list-students.html', {'students': students})
    return redirect('/admin-panel/')


def detail_student(request, student_pk):
    if request.user.is_superuser:
        student = get_object_or_404(User, pk=student_pk)
        return render(request, 'admin-student-details.html', {'student': student})
    return redirect('/admin-panel/')
