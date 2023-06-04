from django.shortcuts import render, redirect
from .models import Task, Table, Group
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def loginPage(request):
    if request.method == 'POST':
        if 'registration' in request.POST:
            return redirect('/registration/')
        username, password = request.POST.get('username'), request.POST.get('password')
        try:
            User.objects.get(username=username)
        except:
            messages.error(request, 'Не существует такого пользователя')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    context = {}
    return render(request, 'base/login.html', context)


def registrationPage(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            return redirect('/login/')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            messages.error(request, 'Ошибка во время регистрации')
    context = {
        'form': UserCreationForm()
    }
    return render(request, 'base/registration.html', context)


def hierarchyPage(request):
    if request.method == 'POST':
        if 'creategroup' in request.POST:
            Group.objects.create(header=request.POST.get('creategroup'))
            return redirect("/hierarchy/")
        elif 'back' in request.POST:
            return redirect('/')
        elif 'deletegroup' in request.POST:
            Group.objects.filter(id=request.POST.get('deletegroup')).delete()
            return redirect("/hierarchy/")
        elif 'createsubgroup' in request.POST:
            group = Group.objects.get(pk=int(request.POST.get('groupid')))
            group.has_subgroup = True
            group.subgroup.add(Group.objects.create(header=request.POST.get('createsubgroup'), is_subgroup=True))
            return redirect("/hierarchy/")
        elif 'deletesubgroup' in request.POST:
            group = Group.objects.get(pk=int(request.POST.get('groupid')))
            group.subgroup.get(id=request.POST.get('deletesubgroup')).delete()
            return redirect("/hierarchy/")
        elif 'split' in request.POST:
            print(request.POST)
            group = Group.objects.get(pk=int(request.POST.get('split')))
            group.has_subgroup = True
            group.save()
            return redirect("/hierarchy/")
        elif 'group' in request.POST:
            print(request.POST)
            group = Group.objects.get(id=request.POST.get('choosedsubgroup'))
            group.users.add(User.objects.get(username=request.POST.get('group')))
            return redirect('/')
    groups = Group.objects.filter(has_subgroup=True) | Group.objects.filter(is_subgroup=False)
    users = User.objects.all()
    context = {'groups': groups,
               'users': users}
    return render(request, 'base/hierarchy.html', context)


def index(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            if 'create' in request.POST:
                print(request.POST.get('create'))
                Task.objects.create(task_text=request.POST.get('create'),
                                    task_table=Table.objects.get(pk=int(request.POST.get('choosedtable'))))
                return redirect("/")
            elif 'delete' in request.POST:
                Task.objects.filter(id=request.POST.get('delete')).delete()
                return redirect("/")
            elif 'createtable' in request.POST:
                table = Table.objects.create(header=request.POST.get('createtable'))
                table.participants.add(request.user)
                return redirect("/")
            elif 'creategroup' in request.POST:
                return redirect('hierarchy/')
            elif 'deletetable' in request.POST:
                Table.objects.filter(id=request.POST.get('deletetable')).delete()
                return redirect("/")
            elif 'logoutUser' in request.POST:
                logout(request)
                return redirect('login/')
            elif 'group' in request.POST:
                table = Table.objects.get(id = request.POST.get('choosedtable'))
                table.TableGroup.add(Group.objects.get(header=request.POST.get('group')))
                return redirect('/')
        if not request.user.is_authenticated:
            return redirect('login/')
        tasks = Task.objects.all()
        tables = Table.objects.filter(participants=request.user)\
                 | Table.objects.filter(TableGroup__in=Group.objects.filter(users=request.user))
        tables = tables.distinct()
        arr = Group.objects.all()
        context = {
            'tasks': tasks,
            'tables': tables,
            'arr': arr
        }
        return render(request, 'base/index.html', context)
    except Task.DoesNotExist:
        return render(request, 'base/index.html')
