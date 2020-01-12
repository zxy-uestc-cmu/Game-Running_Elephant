from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,reverse
from .models import Player, Score, Thoughts
from django.contrib.auth import authenticate, get_user_model, login, logout
from .form import PlayerEditForm, UserRegisterForm, UserLoginForm
from . import scoreboard
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block, FriendshipRequest
from django.contrib.postgres.search import TrigramSimilarity
from django.db import IntegrityError

@login_required
def index(request):
    if request.user.is_authenticated == False:
        return redirect(reverse('hello'))
    return render(request, 'runningelephant/index.html')

def register(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        player = Player(user=user)
        player.save()
        if next:
            return redirect(next)
        return redirect('begin')
    return render(request, "runningelephant/register.html", {'form': form})

@login_required
def profile(request):
    if request.user.is_authenticated == False:
        return redirect(reverse('hello'))
    cxt = {}
    scores = Score.objects.filter(player=request.user.player).order_by('-score')[:5]
    thoughts = Thoughts.objects.filter(player=request.user.player)
    friends = Friend.objects.friends(request.user)
    friend_requests = Friend.objects.requests(request.user)
    cxt['player'] = request.user.player
    cxt['score'] = scores
    cxt['thoughts'] = thoughts
    cxt['friends'] = friends
    cxt['friend_requests'] = friend_requests
    if request.POST and 'personal' in request.POST:
        return redirect(reverse('personal_edit'))
    if request.POST and 'back' in request.POST:
        return redirect(reverse('begin'))
    return render(request, "runningelephant/profile.html", cxt)

@login_required
def personal_edit(request):
    if request.user.is_authenticated == False:
        return redirect(reverse('hello'))
    cxt = {}
    dic = {'img':request.user.player.img,'age':request.user.player.age,'starsign':request.user.player.starsign}
    form = PlayerEditForm(dic)
    if request.POST and 'comfirm' in request.POST:
        form = PlayerEditForm(request.POST,request.FILES,instance=request.user.player)
        if form.is_valid(): 
            form.save()
            return redirect(reverse('profile'))
    cxt['player'] = request.user.player
    cxt['form'] = form
    return render(request, "runningelephant/personal_edit.html", cxt)

@login_required
def thoughts_add(request):
    if request.user.is_authenticated == False:
        return redirect(reverse('hello'))
    if request.POST:
        new_thought = request.POST.get('thoughts')
        curr_player = Player.objects.filter(user=request.user)[0]
        Thoughts.objects.create(player=curr_player, thoughts=new_thought)
        return redirect(reverse('profile'))
    return render(request, "runningelephant/Thoughts.html")

@login_required
def thoughts_delete(request, thought_id):
    data = {'isDelete': True}
    try:
        if request.user.is_authenticated == False:
            return redirect(reverse('hello'))
        Thoughts.objects.get(pk=thought_id).delete()
    except:
        return JsonResponse(data)
    return JsonResponse(data)

def hello(request):
    if request.POST and 'loggin' in request.POST:
        return redirect(reverse('login'))
    elif request.POST and 'signup' in request.POST:
        return redirect(reverse('register'))
    return render(request, "runningelephant/hello.html")

@login_required
def begin(request):
    if request.user.is_authenticated == False:
        return redirect(reverse('hello'))
    if request.POST and 'profile' in request.POST:
        return redirect(reverse('profile'))
    elif request.POST and 'logout' in request.POST:
        return redirect(reverse('logout'))
    elif request.POST and 'score' in request.POST:
        return redirect(reverse('scoreboard'))
    elif request.POST and 'game' in request.POST:
        return redirect(reverse('index'))
    return render(request, "runningelephant/begin.html")

def handle_scoreboard(request):
    """
    dispatch the scoreboard requests
    """
    if request.POST:
        print('Condole: scoreboard -> post')
        return scoreboard.refresh()
    else:
        print('Condole: scoreboard -> get')
        return scoreboard.get_scoreboard(request)

def game_over(request):
    print("CONSOLE: game_over")
    if request.is_ajax():
        score = request.POST['score']
        player = Player.objects.get(user=request.user)
        newScore = Score(score=score, player=player)
        newScore.save()
        data = {'added': True}
        return JsonResponse(data)
    else:
        scores = Score.objects.filter(player=request.user.player).order_by("-time")
        s = scores.first()
        print (s)
        return render(request, "runningelephant/gameover.html", {'score':s})
        
@login_required
def add_friends(request):
    if 'search' in request.GET:
        search_term = request.GET['search']
        friends = Friend.objects.friends(request.user)
        search_result = User.objects.filter(username__icontains=search_term).exclude(username=request.user.username)
        search_result = search_result.exclude(username__in=friends)
        return render(request, "runningelephant/addfriend.html", {'search_result': search_result})
    return render(request, "runningelephant/addfriend.html" )

@login_required
def friend_profile(request, friend_id):
    cxt = {}
    friend = User.objects.get(pk=friend_id)
    scores = Score.objects.filter(player=friend.player).order_by('-score')[:5]
    thoughts = Thoughts.objects.filter(player=friend.player)
    friends = Friend.objects.friends(friend)
    cxt['player'] = friend.player
    cxt['score'] = scores
    cxt['thoughts'] = thoughts
    cxt['friends'] = friends
    return render(request, "runningelephant/friend_profile.html", cxt)

@login_required
def friend_accept(request, friend_request_id):
    try:
        friend_request = FriendshipRequest.objects.get(id=friend_request_id)
        friend_request.accept()
    except:
        return redirect(reverse('profile'))
    return redirect(reverse('profile'))

@login_required
def friend_reject(request, friend_request_id):
    try:
        friend_request = FriendshipRequest.objects.get(id=friend_request_id)
        friend_request.reject()
        friend_request.delete()
    except:
        return redirect(reverse('profile'))
    return redirect(reverse('profile'))

@login_required
def friend_add(request, friend_id):
    other_user = User.objects.get(pk=friend_id)
    try:
        Friend.objects.add_friend(
            request.user,                               # The sender
            other_user,                                 # The recipient
            message='Hi! I would like to add you')      # This message is optional
    except IntegrityError:
        return redirect(reverse('addfriends'))
    else:
        return redirect(reverse('addfriends'))

@login_required
def friend_delete(request, friend_id):
    data = {'deleted': True}
    try:
        other_user = User.objects.get(pk=friend_id)
        Friend.objects.remove_friend(request.user, other_user)
    except:
        return JsonResponse(data)
    return JsonResponse(data)