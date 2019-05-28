from __future__ import absolute_import

from random import randrange

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect

#from PumpManager.pumpdb import convertSongs, getMixes
from PumpManager.models import Song, Chart, Mix, Version, Stage, Player, Location

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm

# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login


from django.views.generic.base import View
from django.contrib.auth import logout

from celery.decorators import task

from django.db.models import Max

from PumpManager.tasks import upgr_db
#from testproj.tasks import add, update_db

#bgu.delay(100,100)
'''
@task(name="sum_two_numbers")
def long_work(x, y):
    a = 0
    for i in range(x*y+100000):
        a = 1+i
    print(a)
    return a
'''

class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "PumpManager/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "PumpManager/login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)
        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")


def index(request):
    return render(request, 'PumpManager/index.html')

def profile(request):
    return render(request, 'PumpManager/profile.html',
    {'context': {"songs_played" : len(request.user.player.stage_set.all())}})

def profile_settings(request):
    return render(request, 'PumpManager/profile-settings.html',)

def uniqueProfile(request, nickname):
    return HttpResponse("You are %s." % nickname)

def statistic(request):
    template = loader.get_template('PumpManager/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def lists(request):
    return render(request, 'PumpManager/lists.html')


#print("ALLO", songs[0][0])
#songs = pumpdb.getSongs()
#songs = convertSongs(songs)
#print("SONGS", songs)
'''
for song in songs:
    models.Song(name=song['name'],
        author = song['author'],
        bpm = song['bpm'],
        type = song['type'],
        cathegory = song['cathegory'],
        ).save()
'''

def songs(request):
    context = ''
    songs =  Song.objects.all()
    charts = []
    for song in songs:
        charts.append(song.chart_set.all())

    if request.method == 'GET':
        print("GET_Method")
        #return render(request, 'PumpManager/songs.html', {'songs': Song.objects.all()})
    elif request.method == 'POST':
        #print(dir(request.POST))
        if "Update song list" in request.POST.keys():
            upgr_db.delay()

        elif "Filter songs" in request.POST.keys():
            if request.POST["type"] != "---":
                songs = songs.filter(type = request.POST["type"])#.filter
            if request.POST["genre"] != "---":
                songs = songs.filter(cathegory = request.POST["genre"])

            charts = []
            if request.POST["mode"] == "Co-op":
                for song in songs:
                    res = song.chart_set.filter(type = "C")
                    if res:
                        charts.append(res)
            else:
                if request.POST["min_diff"] != "---" and request.POST["max_diff"] != "---":
                    for song in songs:
                        res = song.chart_set.filter(lvl__range =
                        (int(request.POST["min_diff"]), int(request.POST["max_diff"])))
                        if res:
                            charts.append(res)
                elif request.POST["min_diff"] != "---":
                    pass
                elif request.POST["max_diff"] != "---":
                    pass
                else:
                    for song in songs:
                        charts.append(song.chart_set.all())

            conv_charts = []
            if request.POST["mode"] == "Single":
                for song in charts:
                    res = song.filter(type = "S")
                    if res:
                        conv_charts.append(res)
                charts = conv_charts
            elif request.POST["mode"] == "Double":
                for song in charts:
                    res = song.filter(type = "D")
                    if res:
                        conv_charts.append(res)
                charts = conv_charts

            songs = []
            for chart in charts: #array of chart arrays
                songs.append(Song.objects.get(name = chart[0].song.name))

            print(songs)
    context = dict(pairs = zip(songs, charts))

    return render(request, 'PumpManager/songs.html',
        {'songs': songs,
        'charts': charts,
        'context': context})



def songID(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
        message = ""
        if request.user.is_authenticated:
            message_ls = list()
            chart_ls = list()
            for chart in Chart.objects.filter(song = Song.objects.get(pk=song_id)):
                res = request.user.player.stage_set.filter(chart = chart)
                chart_ls.append(chart)
                if res:
                    message_ls.append(
                    res.filter(
                    score = res.aggregate(
                    Max('score'))['score__max'])[0])
                else:
                    message_ls.append("")


        print(message)

        context = dict(pairs = zip(chart_ls, message_ls))

    except Song.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'PumpManager/songID.html', {'song': song, 'context': context})

#def songID(request, song_id):
#    return HttpResponse("Hi response")

def mixes(request):
    if request.method == 'GET':
        return render(request, 'PumpManager/mixes.html',
            {'mixes': Mix.objects.all(), 'versions' : Version.objects.all()})

    elif request.method == 'POST':
        mixes = getMixes()
        for mix in mixes:
            m = Mix(name = mix['name'])
            m.save()
            for version in mix['versions']:
                v = Version(mix = m, version = version)
                v.save()

        #for mix in mixes:

        return render(request, 'PumpManager/mixes.html',
            {'mixes': Mix.objects.all(), 'versions': Version.objects.all()})

def mixID(request, mix_id):
        return render(request, 'PumpManager/mixID.html',
                        {'mix': Mix.objects.get(pk=mix_id)})


def random(request):
    if request.method == "GET":
        return render (request, 'PumpManager/random.html',
                        {"message" : "",
                        "result_songs" : [],
                         "versions" : Mix.objects.all()})

    elif request.method == "POST":
        #print(request.POST["mod"], "type", "genre", "min_diff", "max_diff"))
        for key in request.POST.keys():
            print(request.POST[key])

        songs = Song.objects.all()
        if request.POST["type"] != "---":
            songs = songs.filter(type = request.POST["type"])#.filter
        if request.POST["genre"] != "---":
            songs = songs.filter(cathegory = request.POST["genre"])

        charts = []
        if request.POST["mode"] == "Co-op":
            for song in songs:
                res = song.chart_set.filter(type = "C")
                if res:
                    charts.append(res)
        else:
            if request.POST["min_diff"] != "---" and request.POST["max_diff"] != "---":
                for song in songs:
                    res = song.chart_set.filter(lvl__range =
                    (int(request.POST["min_diff"]), int(request.POST["max_diff"])))
                    if res:
                        charts.append(res)
            elif request.POST["min_diff"] != "---":
                pass
            elif request.POST["max_diff"] != "---":
                pass
            else:
                charts.append(Chart.objects.all())

        conv_charts = []
        if request.POST["mode"] == "Single":
            for song in charts:
                conv_charts.append(song.filter(type = "S"))
            charts = conv_charts
        elif request.POST["mode"] == "Double":
            for song in charts:
                conv_charts.append(song.filter(type = "D"))
            charts = conv_charts

        res_song_charts = charts[randrange(len(charts))]
        result = res_song_charts[randrange(res_song_charts.count())]
            #if request.POST["min_diff"] != "---":
            #__gte __lte
        return render (request, 'PumpManager/random.html',
                        {"message" : "Ваш результат:",
                         "result_songs" : songs,
                         "versions" : Mix.objects.all(),
                         "result" : result})

def locations(request):
    return render(request, "PumpManager/locations.html", {"locations": Location.objects.all()})
# Create your views here.
