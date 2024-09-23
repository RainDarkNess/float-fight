import json
import os
import random

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import random

from .forms import RegistrationForm, LoginForm, SessionForm, SessionSet
from .models import Users
from .models import Session

global matrix


def createSession(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            try:
                session_tmp = Session.objects.get(name_session=form.cleaned_data['Имя_сессии'])
                return render(request, 'session.html', {'warning': "Комната уже существует", 'form': form})
            except:
                session = form.save(commit=False)
                session.set_name(form.cleaned_data['Имя_сессии'])
                session.set_player_one(form.cleaned_data['Имя_игрока'])

                set_cookie(request, form.cleaned_data['Имя_игрока'])
                session.set_ship_count_player_one(10)
                session.set_matrix([[1 for _ in range(10)] for _ in range(10)])
                session.save()

                username = request.COOKIES.get('username')

                if not username:
                    response = HttpResponseRedirect("/startSession/" + str(session.id))
                    response.set_cookie('username', form.cleaned_data['Имя_игрока'] + "_one", max_age=3600)
                    return response

                return redirect('start_session_with_id', session_id=session.id)
    else:
        form = SessionForm()
    return render(request, 'session.html', {'form': form})


def get_matrix(request, session_id):
    enemy_name = str(session_id).split("_")[1]
    session_id = int(str(session_id).split("_")[0])
    session = get_object_or_404(Session, id=session_id)

    player_one = session.get_name_player_one()
    matrix = session.get_matrix() if enemy_name == player_one else session.get_matrix_player_two()
    matrix = [[1 if cell == 3 else cell for cell in row] for row in matrix]
    return JsonResponse({'matrix': matrix})


def set_matrix(request, session_id):
    enemy_name = str(session_id).split("_")[1]
    x = int(str(session_id).split("_")[2])
    y = int(str(session_id).split("_")[3])
    session_id = int(str(session_id).split("_")[0])
    session = Session.objects.get(pk=session_id)
    player_one = session.get_name_player_one()
    data = json.loads(request.body)
    new_matrix = data.get('matrix')

    matrix_to_view = new_matrix
    matrix = session.get_matrix() if enemy_name == player_one else session.get_matrix_player_two()
    if matrix[x][y] == 3:
        matrix[x][y] = 0
        session.set_matrix(matrix) if enemy_name == player_one else session.set_matrix_player_two(matrix)
        matrix_to_view[x][y] = 0
    else:
        matrix[x][y] = 2
        session.set_matrix(matrix) if enemy_name == player_one else session.set_matrix_player_two(matrix)
        matrix_to_view[x][y] = 2
    session.save()

    return JsonResponse({'matrix': matrix_to_view})


def get_matrix_MY(request, session_id):
    pleyr_name = str(session_id).split("_")[1]
    session_id = int(str(session_id).split("_")[0])
    session = get_object_or_404(Session, id=session_id)

    username = request.COOKIES.get('username')
    matrix = session.get_matrix() if str(username).split('_')[1] == 'one' else session.get_matrix_player_two()
    return JsonResponse({'matrix': matrix})


def set_matrix_MY(request, session_id):
    pleyr_name = str(session_id).split("_")[1]
    x = int(str(session_id).split("_")[2])
    y = int(str(session_id).split("_")[3])

    session_id = int(str(session_id).split("_")[0])
    session = Session.objects.get(pk=session_id)
    player_one = session.get_name_player_one()

    username = request.COOKIES.get('username')
    count_ships = session.get_ship_count_player_one() if str(username).split('_')[1] == 'one' else session.get_ship_count_player_two()
    matrix = session.get_matrix() if str(username).split('_')[1] == 'one' else session.get_matrix_player_two()
    print(matrix[x][y])

    if count_ships != 0:
        if matrix[x][y] == 1:
            if count_ships > 0:
                session.set_ship_count_player_one(session.get_ship_count_player_one() - 1) if str(username).split('_')[1] == 'one' else session.set_ship_count_player_two(session.get_ship_count_player_two() - 1)
                matrix[x][y] = 3
                session.set_matrix(matrix) if pleyr_name == player_one else session.set_matrix_player_two(matrix)
                session.save()
                matrix = session.get_matrix() if str(username).split('_')[1] == 'one' else session.get_matrix_player_two()
        else:
            session.set_ship_count_player_one(session.get_ship_count_player_one() + 1) if str(username).split('_')[1] == 'one' else session.set_ship_count_player_two(session.get_ship_count_player_two() + 1)
            matrix[x][y] = 1
            session.set_matrix(matrix) if pleyr_name == player_one else session.set_matrix_player_two(matrix)
            session.save()
            matrix = session.get_matrix() if str(username).split('_')[1] == 'one' else session.get_matrix_player_two()

    return JsonResponse({'matrix': matrix, 'player_ship_count': count_ships})


def userChoose(request):
    if request.method == 'POST':
        form = SessionSet(request.POST)
        if form.is_valid():
            name_session = form.cleaned_data['Имя_сессии']
            name_player = form.cleaned_data['Имя_игрока']
            session = Session.objects.get(name_session=name_session)
            session.set_player_two(name_player)
            session.set_ship_count_player_two(10)
            session.set_matrix_player_two([[1 for _ in range(10)] for _ in range(10)])
            session.save()
            username = request.COOKIES.get('username')

            if not username:
                response = HttpResponseRedirect("/startSession/" + str(session.id))
                response.set_cookie('username', form.cleaned_data['Имя_игрока'] + "_two", max_age=3600)
                return response

            return redirect('start_session_with_id', session_id=session.id)
    else:
        form = SessionSet()
    return render(request, 'choose.html', {'form': form})


def set_cookie(request, name):
    username = request.COOKIES.get('username')
    if not username:
        response = HttpResponse("Cookie has been set!")
        response.set_cookie('username', name, max_age=3600)
        return response
    else:
        return render(request, 'choose.html')


def startSession(request, session_id=0, isOwner=True):
    session = Session.objects.get(pk=session_id)
    username = request.COOKIES.get('username')
    matrix = session.get_matrix() if str(username).split('_')[1] == 'one' else session.get_matrix_player_two()
    matrix_enemy = session.get_matrix_player_two() if str(username).split('_')[1] == 'one' else session.get_matrix()
    matrix_enemy = [[1 if cell == 3 else cell for cell in row] for row in matrix_enemy]
    ship_count = session.get_ship_count_player_one() if str(username).split('_')[
                                                            1] == 'one' else session.get_ship_count_player_two()
    player_name = session.get_name_player_one() if str(username).split('_')[
                                                       1] == 'one' else session.get_name_player_two()
    enemy_name = session.get_name_player_two() if str(username).split('_')[
                                                      1] == 'one' else session.get_name_player_one()

    # session.get_matrix_player_two() if len(
    #     session.get_matrix_player_two()) >= 0 else "'NONE'"
    return render(request, "overview.html",
                  context={"matrix": matrix, "matrix_enemy": matrix_enemy, "session_id": session_id,
                           "room_name": session.get_room_name(),
                           "player_name": player_name, "enemy_name": enemy_name,
                           "player_ship_count": ship_count})


def toSession(request, session_id=0):
    session = Session.objects.get(pk=session_id)

    return render(request, "overview.html",
                  context={"matrix": session.get_matrix_player_two() if len(
                      session.get_matrix_player_two()) >= 0 else "'NONE'", "matrix_enemy": session.get_matrix(),
                           "session_id": session_id,
                           "room_name": session.get_room_name(),
                           "player_name": session.get_name_player_two(), "enemy_name": session.get_name_player_one()})
