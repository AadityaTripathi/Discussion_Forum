from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

# rooms=[
#     {'id':1,"name":"Python Forum"},
#     {'id':2,"name":"Java Forum"},
#     {'id':3,"name":"Javascript Forum"},
# ]

def loginPage(request) :
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try :
            user = User.objects.get(username=username)
        except :
            messages.error(request, 'User does not exist')
        
        user = authenticate(request,username = username, password = password)
        
        if user is not None :
            login(request,user)
            return redirect('home')
        else :
            messages.error(request, 'Username or password does not exist')
    
    context = {}
    return render(request,'base/login_register.html', context)

def logoutUser(request) :
    logout(request)
    return redirect('home')


def home(request):       
    #return HttpResponse("Home page")
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topics__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )
    
    room_count = rooms.count()
    #rooms=Room.objects.all()
    topics = Topic.objects.all()
    context={'rooms' : rooms, 'topics' : topics, 'room_count' : room_count}
    return render(request,"base/home.html",context=context)

def room(request, pk):  #primary key
    #return HttpResponse("Room")
    # room=None
    # for i in rooms:
    #     if i["id"]==int(pk) :
    #         room =i
    room = Room.objects.get(id=pk)
    context = {'room' :room}
    return render(request,"base/room.html",context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST' :
        form = RoomForm(request.POST)
        if form.is_valid() :
            form.save() 
            return redirect('home')
        #print(request.POST)
    context={'form' : form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host :
        return HttpResponse("You are not allowed to update this room")
    
    if request.method == 'POST' :
        form = RoomForm(request.POST,instance=room)
        if form.is_valid() :
            form.save()
            return redirect('home')
    
    context={'form' : form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk) :
    room = Room.objects.get(id = pk)
    if request.method == 'POST' :
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj' : room})