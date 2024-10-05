import datetime
import json
import os
import random

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import random

from .forms import RegistrationForm, LoginForm, SessionForm, SessionSet, ArticleAdd, RestoreForm, codeCheck, \
    EditPasswordForm
from .models import Users, restartCode
from .models import Session
from .models import Article

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

global matrix

sender_email_my = 'hurtin5@yandex.ru'
# sender_email_my = 'hurtin5'
sender_password_my = 'dkxlaolrwrrrvewz'
# sender_password_my = 'urrkxeqbrymbrcso'

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
    count_ships = session.get_ship_count_player_one() if str(username).split('_')[
                                                             1] == 'one' else session.get_ship_count_player_two()
    matrix = session.get_matrix() if str(username).split('_')[1] == 'one' else session.get_matrix_player_two()
    print(matrix[x][y])

    if count_ships != 0:
        if matrix[x][y] == 1:
            if count_ships > 0:
                session.set_ship_count_player_one(session.get_ship_count_player_one() - 1) if str(username).split('_')[
                                                                                                  1] == 'one' else session.set_ship_count_player_two(
                    session.get_ship_count_player_two() - 1)
                matrix[x][y] = 3
                session.set_matrix(matrix) if pleyr_name == player_one else session.set_matrix_player_two(matrix)
                session.save()
                matrix = session.get_matrix() if str(username).split('_')[
                                                     1] == 'one' else session.get_matrix_player_two()
        else:
            session.set_ship_count_player_one(session.get_ship_count_player_one() + 1) if str(username).split('_')[
                                                                                              1] == 'one' else session.set_ship_count_player_two(
                session.get_ship_count_player_two() + 1)
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


def helloWorld(request):
    return render(request, "helloworld.html", context={"HelloWorld": "HelloWorld"})


def article(request, article_id):
    article = Article.objects.get(pk=article_id)
    label = article.getLabel()
    body = article.getBody()
    date = article.getDatePublish()
    author = article.getAuthor()
    username = request.COOKIES.get('username')
    canEdit = ""
    try:
        user = Users.objects.get(login=username)
        username = user.get_username()
        if username == author:
            canEdit = '<a href="/redacting/' + str(article.id) + '/">Редактировать</a>'

            return render(request, "article.html",
                          context={"Label": label, "Body": body, "Date": date, "username": author, "canEdit": canEdit})
        else:
            return render(request, "article.html",
                          context={"Label": label, "Body": body, "Date": date, "username": author})
    except:
        return render(request, "article.html", context={"Label": label, "Body": body, "Date": date, "username": author})


def addArticle(request):
    form = ArticleAdd(request.POST)
    if form.is_valid():

        # article = form.save(commit=False)
        label = form.cleaned_data["Название_статьи"]
        body = form.cleaned_data["Содержание"]
        date = datetime.datetime.now()
        username = request.COOKIES.get('username')
        article = Article.objects.create(label=label, body=body, datePublish=date, author=username)
        article.save()
        # response = HttpResponseRedirect("/article/"+str(article.id))
        # return response
        return redirect('article', article_id=article.id)

    else:
        form = ArticleAdd()
    try:
        username = request.COOKIES.get('username')
        user = Users.objects.get(login=username)
    except:
        return redirect('/')
    # return render(request, 'articleAdd.html', {'form': form})
    return render(request, 'allForm.html',
                  {'form': form, 'pageTitle': 'Добавить статью', 'formTitle': 'Добавить статью',
                   'buttonName': 'Добавить',
                   'other': '<a style="display: block; text-align: center; margin-top: 10px" href="/getAllArticles/">Перейти ко всем статьям</a>'})


def getAllArticles(request):
    all_articles = Article.objects.all()
    render_article = ""
    author = ""
    for i in range(len(all_articles)):
        if all_articles[i].author != "":
            author = ' автор статьи: ' + all_articles[i].author
        render_article = render_article + '<a href="/article/' + str(all_articles[i].id) + '/">' + all_articles[
            i].label + ' дата публикации:' + str(all_articles[i].datePublish).split(" ")[0].replace("-",
                                                                                                    ".") + author + '</a>' + '<br>'
    print(render_article)
    return render(request, 'allArticles.html', {"render_article": render_article})


def register(request):
    response = HttpResponseRedirect("/getAllArticles/")
    if response.cookies.get("username") is not None:
        return response
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.clean()
            user.set_username(form.cleaned_data["Логин"])
            user.set_password(form.cleaned_data['Пароль'])
            user.setEmail(form.cleaned_data['Email'])
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'allForm.html',
                  {'form': form, 'pageTitle': 'Зарегистрироваться', 'formTitle': 'Зарегистрироваться',
                   'buttonName': 'Зарегистрироваться',
                   'other': '<a href="login/" style="text-align: center; width: 100%; display: block; padding-top: 10px">Войти</a><a style="display: block; text-align: center; margin-top: 10px" href="/getAllArticles/">Перейти ко всем статьям</a>'})


def restoreAccount(request):
    if request.method == 'POST':
        form = RestoreForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            try:
                body = ''
                user = get_object_or_404(Users, email=email)
                for i in range(4):
                    body += str(random.randint(0, 9))
                print(body)
                # send_email(sender_email_my, sender_password_my, email, "Восстановление пароля", body)
                code = restartCode.objects.create(restart_code=body)
                return redirect('/codeCheckFun/'+str(user.id))
            except Exception as e:
                print(e)
                return redirect('restore-account')
    else:
        form = RestoreForm()
    # return render(request, 'codeSend.html', {'form': form})
    return render(request, 'allForm.html',
                  {'form': form, 'pageTitle': 'Отправить код на email', 'formTitle': 'Отправить код на email',
                   'buttonName': 'отправить',
                   'other': '<a href="/login/" style="text-align: center; width: 100%; display: block; padding-top: 10px">Войти</a>'})


def codeCheckFun(request, user_id):
    # if request.method == 'POST':
    form = codeCheck(request.POST)
    if form.is_valid():
        try:
            print(form.cleaned_data['Код_подтверждения'])
            code = get_object_or_404(restartCode, restart_code=form.cleaned_data['Код_подтверждения'])
            code.delete()
            return redirect('/editPass/'+str(user_id))
        except Exception as e:
            return redirect('code-check-fun')

    else:
        form = codeCheck()
    return render(request, 'allForm.html',
                  {'form': form, 'pageTitle': 'Верификация пароля', 'formTitle': 'Верификация пароля',
                   'buttonName': 'Отправить', 'other': ''})


def editPass(request, user_id):
    # if request.method == 'POST':
    form = EditPasswordForm(request.POST)
    if form.is_valid():
        try:
            username = request.COOKIES.get('username')
            user = Users.objects.get(id=user_id)
            user.set_password(form.cleaned_data['Пароль'])
            user.save()
            return redirect('login')
        except Exception as e:
            print(e)
            return redirect('')

    else:
        form = EditPasswordForm()
    return render(request, 'allForm.html',
                  {'form': form, 'pageTitle': 'Изменение пароля', 'formTitle': 'Изменить пароль',
                   'buttonName': 'Изменить', 'other': ''})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['Логин']
            password = form.cleaned_data['Пароль']
            try:
                user = Users.objects.get(login=login)
                if user.check_password(password):
                    print(user.id)
                    # request.session['user_id'] = user.id
                    messages.success(request, 'Login successful!')
                    response = HttpResponseRedirect("/getAllArticles/")
                    response.set_cookie('username', user.get_username(), max_age=3600)
                    print(user.get_username())
                    return response
                    # return redirect('choose')
                else:
                    messages.error(request, 'Invalid password')
            except Users.DoesNotExist:
                messages.error(request, 'Invalid login')
    else:
        form = LoginForm()

    # return render(request, 'authform.html', {'form': form})
    return render(request, 'allForm.html',
                  {'form': form, 'pageTitle': 'Войти', 'formTitle': 'Логин', 'buttonName': 'Войти',
                   'other': '<a href="/restoreAccount/" style="text-align: center; width: 100%; display: block; padding-top: 10px">Забыл пароль</a><a style="display: block; text-align: center; margin-top: 10px" href="/getAllArticles/">Перейти ко всем статьям</a><a style="display: block; text-align: center; margin-top: 10px" href="/">Зарегистрироваться</a>'})


def redacting(request, article_id):
    form = ArticleAdd(request.POST)
    if form.is_valid():
        # article = form.save(commit=False)
        label = form.cleaned_data["Название_статьи"]
        body = form.cleaned_data["Содержание"]
        date = datetime.datetime.now()
        article = get_object_or_404(Article, id=article_id)
        article.setLabel(label)
        article.setBody(body)
        article.setDatePublish(date)
        article.save()
        return redirect('article', article_id=article_id)
    else:
        form = ArticleAdd()
    return render(request, 'edit.html', {'form': form})


def logout(request):
    request.session.flush()  # Удаляет все данные из сессии
    messages.success(request, 'You have been logged out')
    return redirect('login')


def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Создаем сообщение
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    print(sender_email)
    print(sender_password)
    try:
        server = smtplib.SMTP('smtp.yandex.ru', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Отправляем письмо
        server.send_message(msg)
        print("Email отправлен успешно!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        server.quit()
