import json
import os
import random

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import random

from .forms import RegistrationForm, LoginForm, SessionForm, SessionSet
from .models import Users
from .models import Session

global matrix


def index(request):
    global result
    matrix = [
        [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    return render(request, 'authform.html')
    # return render(request, "overview.html", context={"matrix": matrix})


def createSession(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.set_name(form.cleaned_data['name_session'])
            session.set_matrix([[1 for _ in range(6)] for _ in range(6)])
            session.save()
            return redirect('start_session_with_id', session_id=session.id)
    else:
        form = SessionForm()
    return render(request, 'session.html', {'form': form})


def get_matrix(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    return JsonResponse({'matrix': session.get_matrix()})


def set_matrix(request, session_id):
    session = Session.objects.get(pk=session_id)
    data = json.loads(request.body)
    new_matrix = data.get('matrix')
    session.set_matrix(new_matrix)
    session.save()
    session = Session.objects.get(pk=session_id)
    return JsonResponse({'matrix': session.get_matrix()})


def userChoose(request):
    if request.method == 'POST':
        form = SessionSet(request.POST)
        if form.is_valid():
            name_session = form.cleaned_data['name_session']
            session = Session.objects.get(name_session=name_session)
            return redirect('start_session_with_id', session_id=session.id)
    else:
        form = SessionSet()
    return render(request, 'choose.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            try:
                user = Users.objects.get(login=form.cleaned_data['login'])
                return redirect('login')
            except:
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, 'Registration successful!')
                return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            try:
                user = Users.objects.get(login=login)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    messages.success(request, 'Login successful!')
                    return redirect('choose')
                else:
                    messages.error(request, 'Invalid password')
            except Users.DoesNotExist:
                messages.error(request, 'Invalid login')
    else:
        form = LoginForm()
    return render(request, 'authform.html', {'form': form})


def logout(request):
    request.session.flush()  # Удаляет все данные из сессии
    messages.success(request, 'You have been logged out')
    return redirect('login')


def startSession(request, session_id=0):
    session = Session.objects.get(pk=session_id)
    # matrix = [
    #     [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0]
    # ]
    matrix = session.get_matrix()
    # x = random.randint(0, 5)
    # y = random.randint(0, 5)
    # if matrix[x][y] == 0:
    #     matrix[x][y] = 1
    return render(request, "overview.html", context={"matrix": matrix, "session_id": session_id})
